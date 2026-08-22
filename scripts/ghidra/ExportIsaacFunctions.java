// Headless Ghidra script: rename and decompile selected statically identified functions.
// @category IsaacOffline

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSet;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.listing.FlowOverride;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import ghidra.program.model.symbol.SourceType;

import java.io.File;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.HashSet;
import java.util.Set;
import java.util.TreeSet;

public class ExportIsaacFunctions extends GhidraScript {
    private static final Map<String, String> TARGETS = new LinkedHashMap<>();
    private static final Map<String, String> FORCED_BODY_ENDS = new LinkedHashMap<>();

    static {
        TARGETS.put("Seeds__constructor", "009e9290");
        TARGETS.put("Seeds__IsStringValidSeed", "009eb590");
        TARGETS.put("Seeds__Seed2String", "009eb5b0");
        TARGETS.put("Seeds__String2Seed", "009eb6b0");
        TARGETS.put("Seeds__set_start_seed", "009eb880");
        TARGETS.put("Seeds__advance_stage_slot", "009eb980");
        TARGETS.put("RNG__game_constructor", "007e8f90");
        TARGETS.put("RNG__SetSeed", "007e8fe0");
        TARGETS.put("RNG__RandomInt", "007e9020");
        TARGETS.put("RNG__RandomFloat", "007e9080");
        TARGETS.put("RNG__Next", "007e90f0");
        TARGETS.put("Game__update_current_room_state", "00802980");
        TARGETS.put("Isaac__log", "00a112c0");
        TARGETS.put("LevelGenerator_Room__constructor", "007381b0");
        TARGETS.put("Level__Init", "00744940");
        TARGETS.put("Level__Init_helper_738650", "00738650");
        TARGETS.put("Level__attempt_reset", "007382c0");
        TARGETS.put("Level__Init_helper_745b70", "00745b70");
        TARGETS.put("Level__can_apply_labyrinth", "007385c0");
        TARGETS.put("Level__curse_mode_predicate", "006f8120");
        TARGETS.put("Level__normalize_curse_mask", "00864ae0");
        TARGETS.put("Level__combined_curse_add_mask", "006f9400");
        TARGETS.put("Level__combined_curse_remove_mask", "006f95a0");
        TARGETS.put("Level__alt_path_first_half_predicate", "0074ef70");
        TARGETS.put("Level__alt_path_second_half_predicate", "0074efd0");
        TARGETS.put("Level__alt_path_first_half_finalize", "0074f0c0");
        TARGETS.put("Level__alt_path_second_half_finalize", "0074f360");
        TARGETS.put("Level__set_stage_and_type", "007466d0");
        TARGETS.put("Level__pre_init_alt_fixup", "007467c0");
        TARGETS.put("Level__query_room_config", "0082ce40");
        TARGETS.put("Level__get_room_config_stage", "0082d030");
        TARGETS.put("RoomConfig__select_room", "0082c7d0");
        TARGETS.put("RoomConfig__select_room_with_stage", "0082cdd0");
        TARGETS.put("RoomConfig__get_room", "0082c720");
        TARGETS.put("RoomConfig__exact_door_predicate", "006da750");
        TARGETS.put("RNG__inline_seed_helper", "00428940");
        TARGETS.put("Level__find_room_type_state", "004288a0");
        TARGETS.put("Level__select_boss_id", "00422830");
        TARGETS.put("BossPool__bosspools_xml_consumer", "00421a20");
        TARGETS.put("BossPool__entry_is_removed", "00421720");
        TARGETS.put("BossPool__entry_is_available", "004217a0");
        TARGETS.put("BossPool__PickBoss", "00422620");
        TARGETS.put("BossPool__commit_floor", "00421b50");
        TARGETS.put("BossPool__bitset_buffer_reserve", "0041c910");
        TARGETS.put("BossPool__bitset_buffer_fill", "0041cb90");
        TARGETS.put("BossPool__shuffle_runtime_init", "008f4890");
        TARGETS.put("BossPool__shuffle_seed", "008fd3c0");
        TARGETS.put("BossPool__shuffle_next", "008fd410");
        TARGETS.put("Game__boss_pool_init_caller", "006f8140");
        TARGETS.put("Game__boss_pool_state_loader", "0068cdc0");
        TARGETS.put("PlayerManager__FirstCollectibleOwner", "009be080");
        TARGETS.put("PlayerManager__condition_9be630", "009be630");
        TARGETS.put("PlayerManager__condition_9be6b0", "009be6b0");
        TARGETS.put("PlayerManager__condition_9beb30", "009beb30");
        TARGETS.put("PlayerManager__condition_9bf930", "009bf930");
        TARGETS.put("PlayerManager__condition_7cb6e0", "007cb6e0");
        TARGETS.put("PlayerManager__get_player_417870", "00417870");
        TARGETS.put("PersistentState__condition_423250", "00423250");
        TARGETS.put("Game__GetPlanetariumChance", "0074dbd0");
        TARGETS.put("Level__condition_74b5d0", "0074b5d0");
        TARGETS.put("Level__condition_74f030", "0074f030");
        TARGETS.put("LevelGenerator__constructor", "009adaf0");
        TARGETS.put("LevelGenerator__Generate", "009adbb0");
        TARGETS.put("Level__generate_dungeon", "00740e10");
        TARGETS.put("Level__place_post_topology_rooms", "00739370");
        TARGETS.put("Level__assign_room_config", "00738ab0");
        TARGETS.put("Level__select_start_room_config", "00739080");
        TARGETS.put("Level__unknown_special_generator", "0074fbe0");
        TARGETS.put("Level__unknown_special_generator_caller", "007508c0");
        TARGETS.put("Level__room_config_candidate_cleanup", "007527b0");
        TARGETS.put("Level__build_secret_candidate_set", "00738d70");
        TARGETS.put("LevelGenerator__CreateRoom", "009add30");
        TARGETS.put("LevelGenerator__late_default_candidate", "009addf0");
        TARGETS.put("LevelGenerator__GetNewEndRoom", "009ae0e0");
        TARGETS.put("LevelGenerator__PlaceSecretRoom", "009ae170");
        TARGETS.put("LevelGenerator__PlaceUltraSecretRoom", "009ae640");
        TARGETS.put("LevelGenerator__DetermineBossRoom", "009aed50");
        TARGETS.put("LevelGenerator__post_topology_dispatch", "009aef10");
        TARGETS.put("LevelGenerator__room_matches_mask", "009b1220");
        TARGETS.put("LevelGenerator__collect_rooms", "009af0e0");
        TARGETS.put("LevelGenerator__erase_dead_end", "009b1910");
        TARGETS.put("LevelGenerator__copy_room_vector", "009b1950");
        TARGETS.put("LevelGenerator__force_new_dead_end", "009af1e0");
        TARGETS.put("LevelGenerator__has_shape_slot", "009af370");
        TARGETS.put("LevelGenerator__get_door_source_position", "009af3f0");
        TARGETS.put("LevelGenerator__get_door_target_position", "009af620");
        TARGETS.put("LevelGenerator__mark_dead_ends", "009afb10");
        TARGETS.put("LevelGenerator__classify_dead_ends", "009afc70");
        TARGETS.put("LevelGenerator__get_room_placement_offsets", "009afdb0");
        TARGETS.put("LevelGenerator__canonical_grid_index", "009afd70");
        TARGETS.put("LevelGenerator__is_pos_free", "009b0180");
        TARGETS.put("LevelGenerator__is_placement_valid", "009b0240");
        TARGETS.put("LevelGenerator__place_room", "009b0330");
        TARGETS.put("LevelGenerator__count_neighbor_links", "009b0440");
        TARGETS.put("LevelGenerator__generate_rooms", "009b04d0");
        TARGETS.put("LevelGenerator__get_neighbor_candidates", "009b0b00");
        TARGETS.put("LevelGenerator__update_room_connections", "009af980");
        TARGETS.put("LevelGenerator__queue_push_front", "009b1a90");
        TARGETS.put("LevelGenerator__shuffle_candidates", "009b1b20");

        // Ghidra's initial noreturn misclassification of Isaac__log left holes
        // in these function bodies. Raw disassembly proves the contiguous
        // entry-to-RET extents below.
        FORCED_BODY_ENDS.put("LevelGenerator__Generate", "009add2a");
        FORCED_BODY_ENDS.put("LevelGenerator__generate_rooms", "009b0af8");
    }

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

        FunctionManager manager = currentProgram.getFunctionManager();
        Function logger = manager.getFunctionAt(toAddr("00a112c0"));
        if (logger == null) {
            throw new IllegalStateException("missing internal logger at 00a112c0");
        }
        // Auto-analysis mistakes this varargs logger for a terminating assert
        // because some zero-RNG callers place INT3 after it. The function itself
        // returns, and treating it as noreturn truncates generator control flow.
        logger.setNoReturn(false);
        ReferenceIterator loggerReferences = currentProgram.getReferenceManager()
            .getReferencesTo(logger.getEntryPoint());
        while (loggerReferences.hasNext()) {
            Reference reference = loggerReferences.next();
            Instruction instruction = currentProgram.getListing()
                .getInstructionAt(reference.getFromAddress());
            if (instruction != null && instruction.getFlowType().isCall()) {
                instruction.setFlowOverride(FlowOverride.NONE);
                if (instruction.getFallThrough() == null) {
                    instruction.setFallThrough(
                        instruction.getAddress().add(instruction.getLength()));
                }
            }
        }
        for (Map.Entry<String, String> target : TARGETS.entrySet()) {
            Address address = toAddr(target.getValue());
            Function function = manager.getFunctionAt(address);
            if (function == null) {
                function = manager.getFunctionContaining(address);
            }
            if (function == null) {
                println("MISSING function at " + address + " for " + target.getKey());
                continue;
            }
            String forcedEnd = FORCED_BODY_ENDS.get(target.getKey());
            if (forcedEnd != null) {
                function.setBody(new AddressSet(address, toAddr(forcedEnd)));
            }
            function.setName(target.getKey(), SourceType.USER_DEFINED);
        }

        DecompInterface decompiler = new DecompInterface();
        decompiler.toggleCCode(true);
        decompiler.toggleSyntaxTree(true);
        decompiler.setSimplificationStyle("decompile");
        if (!decompiler.openProgram(currentProgram)) {
            throw new IllegalStateException("failed to open program in decompiler");
        }

        File indexFile = new File(outputDirectory, "index.tsv");
        try (PrintWriter index = new PrintWriter(indexFile, StandardCharsets.UTF_8)) {
            index.println("name\tentry\tsize\tstatus");
            for (Map.Entry<String, String> target : TARGETS.entrySet()) {
                Address address = toAddr(target.getValue());
                Function function = manager.getFunctionAt(address);
                if (function == null) {
                    function = manager.getFunctionContaining(address);
                }
                if (function == null) {
                    index.println(target.getKey() + "\t" + address + "\t0\tMISSING");
                    continue;
                }

                DecompileResults result = decompiler.decompileFunction(function, 300, monitor);
                String status = result.decompileCompleted() ? "OK" : result.getErrorMessage();
                Address entry = function.getEntryPoint();
                index.println(target.getKey() + "\t" + entry + "\t" +
                    function.getBody().getNumAddresses() + "\t" + status.replace('\t', ' '));

                File output = new File(outputDirectory, target.getKey() + ".c");
                try (PrintWriter writer = new PrintWriter(output, StandardCharsets.UTF_8)) {
                    writer.println("/*");
                    writer.println(" * Static Ghidra decompilation only; the PE was never executed.");
                    writer.println(" * Program SHA-256: 3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b");
                    writer.println(" * Function: " + target.getKey());
                    writer.println(" * Entry: " + entry);
                    writer.println(" * Body bytes/addresses: " + function.getBody().getNumAddresses());
                    writer.println(" * Decompile status: " + status);
                    writer.println(" */");
                    writer.println();
                    writer.println("/* Callers */");
                    Set<String> callers = new TreeSet<>();
                    ReferenceIterator references = currentProgram.getReferenceManager().getReferencesTo(entry);
                    while (references.hasNext()) {
                        Reference reference = references.next();
                        Function caller = manager.getFunctionContaining(reference.getFromAddress());
                        callers.add(caller == null
                            ? reference.getFromAddress().toString()
                            : caller.getName() + " @ " + caller.getEntryPoint());
                    }
                    for (String caller : callers) {
                        writer.println("// " + caller);
                    }
                    writer.println();
                    writer.println("/* Callees */");
                    Set<String> callees = new TreeSet<>();
                    for (Function callee : function.getCalledFunctions(monitor)) {
                        callees.add(callee.getName() + " @ " + callee.getEntryPoint());
                    }
                    for (String callee : callees) {
                        writer.println("// " + callee);
                    }
                    writer.println();
                    if (result.decompileCompleted() && result.getDecompiledFunction() != null) {
                        writer.println(result.getDecompiledFunction().getC());
                    } else {
                        writer.println("/* DECOMPILATION FAILED: " + status + " */");
                    }
                }
            }
        } finally {
            decompiler.dispose();
        }

        File weightSitesFile = new File(outputDirectory, "room_weight_sites.tsv");
        try (PrintWriter sites = new PrintWriter(weightSitesFile, StandardCharsets.UTF_8)) {
            sites.println("function\tentry\tinstruction\ttext");
            FunctionIterator functions = manager.getFunctions(true);
            while (functions.hasNext()) {
                Function function = functions.next();
                boolean sawInitialWeightRead = false;
                boolean sawWeightWrite = false;
                Set<String> rows = new TreeSet<>();
                InstructionIterator instructions = currentProgram.getListing()
                    .getInstructions(function.getBody(), true);
                while (instructions.hasNext()) {
                    Instruction instruction = instructions.next();
                    String destination = instruction.getNumOperands() > 0
                        ? instruction.getDefaultOperandRepresentation(0) : "";
                    String source = instruction.getNumOperands() > 1
                        ? instruction.getDefaultOperandRepresentation(1) : "";
                    String mnemonic = instruction.getMnemonicString();
                    if (source.contains("0x30")) {
                        sawInitialWeightRead = true;
                        rows.add(instruction.getAddress() + "\t" + instruction);
                    }
                    if (mnemonic.startsWith("MOV") && destination.contains("0x34")) {
                        sawWeightWrite = true;
                        rows.add(instruction.getAddress() + "\t" + instruction);
                    }
                }
                if (sawInitialWeightRead && sawWeightWrite) {
                    for (String row : rows) {
                        sites.println(function.getName() + "\t" + function.getEntryPoint() + "\t" + row);
                    }
                }
            }
        }

        File weightCandidatesFile = new File(outputDirectory, "room_weight_candidates.tsv");
        try (PrintWriter candidates = new PrintWriter(weightCandidatesFile, StandardCharsets.UTF_8)) {
            candidates.println("function\tentry\tbase_register\tinstructions");
            FunctionIterator functions = manager.getFunctions(true);
            while (functions.hasNext()) {
                Function function = functions.next();
                Map<String, Set<String>> reads = new LinkedHashMap<>();
                Map<String, Set<String>> writes = new LinkedHashMap<>();
                for (String register : new String[] {"EAX", "EBX", "ECX", "EDX", "ESI", "EDI"}) {
                    reads.put(register, new TreeSet<>());
                    writes.put(register, new TreeSet<>());
                }
                InstructionIterator instructions = currentProgram.getListing()
                    .getInstructions(function.getBody(), true);
                while (instructions.hasNext()) {
                    Instruction instruction = instructions.next();
                    String destination = instruction.getNumOperands() > 0
                        ? instruction.getDefaultOperandRepresentation(0) : "";
                    String source = instruction.getNumOperands() > 1
                        ? instruction.getDefaultOperandRepresentation(1) : "";
                    for (String register : reads.keySet()) {
                        if (source.contains("[" + register + " + 0x30]")) {
                            reads.get(register).add(instruction.getAddress() + " " + instruction);
                        }
                        if (instruction.getMnemonicString().startsWith("MOV") &&
                            destination.contains("[" + register + " + 0x34]")) {
                            writes.get(register).add(instruction.getAddress() + " " + instruction);
                        }
                    }
                }
                for (String register : reads.keySet()) {
                    if (!reads.get(register).isEmpty() && !writes.get(register).isEmpty()) {
                        Set<String> rows = new TreeSet<>();
                        rows.addAll(reads.get(register));
                        rows.addAll(writes.get(register));
                        candidates.println(function.getName() + "\t" + function.getEntryPoint() +
                            "\t" + register + "\t" + String.join(" | ", rows));
                    }
                }
            }
        }
    }
}
