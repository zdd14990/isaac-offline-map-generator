// Headless Ghidra script: statically export callers/references for one address.
// @category IsaacOffline

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;

import java.io.File;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;

public class ExportAddressReferences extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length != 2) {
            throw new IllegalArgumentException("expected target-address and output-directory");
        }
        Address target = toAddr(args[0]);
        File outputDirectory = new File(args[1]);
        if (!outputDirectory.exists() && !outputDirectory.mkdirs()) {
            throw new IllegalStateException("cannot create output directory: " + outputDirectory);
        }

        FunctionManager functions = currentProgram.getFunctionManager();
        Map<Address, Function> callers = new LinkedHashMap<>();
        ReferenceIterator references = currentProgram.getReferenceManager().getReferencesTo(target);
        while (references.hasNext()) {
            Reference reference = references.next();
            Function caller = functions.getFunctionContaining(reference.getFromAddress());
            if (caller != null) {
                callers.put(reference.getFromAddress(), caller);
            }
        }
        if (callers.isEmpty()) {
            Function containing = functions.getFunctionContaining(target);
            if (containing != null) {
                callers.put(target, containing);
            } else {
                FunctionIterator backward = functions.getFunctions(target, false);
                FunctionIterator forward = functions.getFunctions(target, true);
                Function before = backward.hasNext() ? backward.next() : null;
                Function after = forward.hasNext() ? forward.next() : null;
                println("No containing function for " + target
                        + "; before=" + (before == null ? "NONE" : before.getEntryPoint())
                        + "; after=" + (after == null ? "NONE" : after.getEntryPoint()));
                if (before != null) {
                    callers.put(target, before);
                }
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
                Address referenceSite = entry.getKey();
                Function caller = entry.getValue();
                DecompileResults result = decompiler.decompileFunction(caller, 300, monitor);
                String filename = "target_" + target + "_caller_" + caller.getEntryPoint()
                        + "_ref_" + referenceSite + ".c";
                try (PrintWriter writer = new PrintWriter(
                        new File(outputDirectory, filename), StandardCharsets.UTF_8)) {
                    writer.println("/* Static decompilation only; PE entry point was not executed. */");
                    writer.println("/* Target: " + target + " */");
                    writer.println("/* Reference: " + referenceSite + " */");
                    writer.println("/* Caller: " + caller.getName() + " @ "
                            + caller.getEntryPoint() + " */");
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
        println("Exported " + callers.size() + " static references to " + target);
    }
}
