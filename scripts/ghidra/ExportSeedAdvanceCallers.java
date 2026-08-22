// Headless Ghidra script: statically decompile callers of Seeds::advance_stage_slot.
// @category IsaacOffline

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;

import java.io.File;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;

public class ExportSeedAdvanceCallers extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length != 1) {
            throw new IllegalArgumentException("expected one output-directory argument");
        }
        File outputDirectory = new File(args[0]);
        if (!outputDirectory.exists() && !outputDirectory.mkdirs()) {
            throw new IllegalStateException("cannot create output directory: " + outputDirectory);
        }

        Address callee = toAddr("009eb980");
        FunctionManager functions = currentProgram.getFunctionManager();
        Map<Address, Function> callers = new LinkedHashMap<>();
        ReferenceIterator references = currentProgram.getReferenceManager().getReferencesTo(callee);
        while (references.hasNext()) {
            Reference reference = references.next();
            Function caller = functions.getFunctionContaining(reference.getFromAddress());
            if (caller != null) {
                callers.put(reference.getFromAddress(), caller);
            }
        }

        DecompInterface decompiler = new DecompInterface();
        decompiler.toggleCCode(true);
        decompiler.toggleSyntaxTree(true);
        decompiler.setSimplificationStyle("decompile");
        if (!decompiler.openProgram(currentProgram)) {
            throw new IllegalStateException("failed to open program in decompiler");
        }
        try {
            for (Map.Entry<Address, Function> entry : callers.entrySet()) {
                Address callSite = entry.getKey();
                Function caller = entry.getValue();
                DecompileResults result = decompiler.decompileFunction(caller, 300, monitor);
                String filename = "caller_" + caller.getEntryPoint() + "_call_" + callSite + ".c";
                try (PrintWriter writer = new PrintWriter(
                        new File(outputDirectory, filename), StandardCharsets.UTF_8)) {
                    writer.println("/* Static decompilation only; PE entry point was not executed. */");
                    writer.println("/* Caller: " + caller.getName() + " @ " + caller.getEntryPoint() + " */");
                    writer.println("/* advance_stage_slot call site: " + callSite + " */");
                    writer.println();
                    if (result.decompileCompleted() && result.getDecompiledFunction() != null) {
                        writer.println(result.getDecompiledFunction().getC());
                    } else {
                        writer.println("/* DECOMPILATION FAILED: " + result.getErrorMessage() + " */");
                    }
                }
            }
        } finally {
            decompiler.dispose();
        }
        println("Exported " + callers.size() + " static callers to " + outputDirectory);
    }
}
