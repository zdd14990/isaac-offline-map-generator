/* Static decompilation only; PE entry point was not executed. */
/* Caller: Game__boss_pool_state_loader @ 0068cdc0 */
/* advance_stage_slot call site: 006915c3 */


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall
Game__boss_pool_state_loader(int *param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  int iVar1;
  char cVar2;
  char *pcVar3;
  int iVar4;
  undefined4 uVar5;
  uint uVar6;
  basic_string<char,std::char_traits<char>,std::allocator<char>_> *pbVar7;
  int *piVar8;
  uint uVar9;
  char *pcVar10;
  int *piVar11;
  uint uVar12;
  uint uVar13;
  code *pcVar14;
  undefined4 *puVar15;
  uint uVar16;
  int iVar17;
  code *pcVar18;
  uint uVar19;
  double dVar20;
  undefined4 in_stack_fffffd40;
  undefined4 in_stack_fffffd44;
  undefined4 in_stack_fffffd48;
  undefined4 in_stack_fffffd4c;
  undefined4 in_stack_fffffd50;
  undefined4 in_stack_fffffd54;
  undefined4 in_stack_fffffd58;
  undefined4 in_stack_fffffd5c;
  undefined4 in_stack_fffffd60;
  undefined4 in_stack_fffffd64;
  undefined4 in_stack_fffffd68;
  undefined4 in_stack_fffffd6c;
  undefined4 in_stack_fffffd70;
  undefined4 in_stack_fffffd74;
  undefined4 in_stack_fffffd78;
  undefined4 in_stack_fffffd7c;
  undefined4 in_stack_fffffd80;
  undefined4 in_stack_fffffd84;
  undefined4 in_stack_fffffd88;
  undefined4 in_stack_fffffd8c;
  undefined4 in_stack_fffffd90;
  undefined4 in_stack_fffffd94;
  undefined4 in_stack_fffffd98;
  undefined4 uVar21;
  undefined4 uVar22;
  undefined4 uVar23;
  undefined4 uVar24;
  size_t _MaxCount;
  undefined1 local_24c [8];
  undefined1 local_244 [8];
  uint local_23c;
  undefined1 local_238 [4];
  undefined1 local_234 [4];
  uint local_230;
  uint local_22c;
  undefined1 local_224 [4];
  undefined1 local_220 [4];
  uint local_21c;
  undefined8 local_218;
  undefined1 local_20d;
  int *local_20c;
  int local_208;
  code *local_204;
  uint local_200;
  code *local_1fc;
  char local_1f5;
  int local_1f4;
  int local_1f0;
  char local_1e5;
  undefined1 local_1e4 [24];
  undefined1 local_1cc [24];
  undefined1 local_1b4 [24];
  undefined1 local_19c [24];
  basic_string<char,std::char_traits<char>,std::allocator<char>_> local_184 [24];
  undefined1 local_16c [24];
  undefined1 local_154 [24];
  undefined1 local_13c [24];
  undefined1 local_124 [24];
  undefined1 local_10c [24];
  undefined1 local_f4 [24];
  undefined1 local_dc [24];
  basic_string<char,std::char_traits<char>,std::allocator<char>_> local_c4 [12];
  undefined1 local_b8 [4];
  undefined1 local_b4 [8];
  basic_string<char,std::char_traits<char>,std::allocator<char>_> local_ac [24];
  undefined1 local_94 [24];
  basic_string<char,std::char_traits<char>,std::allocator<char>_> local_7c [8];
  undefined4 local_74;
  int local_70;
  int local_6c;
  undefined4 local_68;
  char *local_64 [12];
  undefined1 local_34 [8];
  undefined1 local_2c [24];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;

  local_8 = 0xffffffff;
  puStack_c = &LAB_00af9745;
  local_10 = ExceptionList;
  local_14 = DAT_00bf93b4 ^ (uint)&stack0xfffffffc;
  ExceptionList = &local_10;
  local_208 = param_4;
  local_21c = 0;
  local_20c = param_1;
  FUN_0067f580(0x20,local_14);
  local_8._0_1_ = 0;
  local_8._1_3_ = 0;
  if (param_4 == 0) {
    param_4 = FUN_009b92c0(0);
    local_208 = param_4;
  }
  cVar2 = FUN_004561f0(&DAT_00b65804);
  if ((cVar2 == '\0') || ((uint)((local_1f0 - local_1f4) / 0x18) < 2)) {
    cVar2 = FUN_004561f0("delirious");
    if (cVar2 != '\0') {
      if ((1 < (uint)((local_1f0 - local_1f4) / 0x18)) &&
         (cVar2 = FUN_004561f0(&DAT_00b660ec), cVar2 != '\0')) {
        local_74 = 0;
        local_70 = 0;
        local_6c = 0;
        local_68 = 1;
        FUN_009b92c0(0);
        FUN_005caa70(&local_74,1);
        uVar6 = DAT_00c7166c;
        goto LAB_0069249e;
      }
      uVar6 = FUN_006eef60();
      pcVar18 = (code *)(&DAT_00c33d80 + (uVar6 % 0x3b) * 4);
      local_204 = pcVar18;
      if (1 < (uint)((local_1f0 - local_1f4) / 0x18)) {
        cVar2 = FUN_004561f0(&DAT_00b660ec);
        if (cVar2 == '\0') {
          uVar5 = FUN_004143f0(1);
          FUN_0040cf50(uVar5);
          local_8._0_1_ = 8;
          uVar6 = FUN_00414410();
          if (2 < uVar6) {
            uVar19 = 2;
            uVar6 = FUN_00414410();
            if (2 < uVar6) {
              do {
                uVar5 = FUN_004143f0(uVar19);
                FUN_00421620(&DAT_00b656ec);
                local_8._0_1_ = 9;
                uVar5 = FUN_00651d50(uVar5);
                FUN_004215a0(uVar5);
                thunk_FUN_0040d040();
                local_8._0_1_ = 8;
                thunk_FUN_0040d040();
                uVar19 = uVar19 + 1;
                uVar6 = FUN_00414410();
              } while (uVar19 < uVar6);
            }
          }
          puVar15 = (undefined4 *)FUN_00684e50((int)&local_218 + 4);
          uVar5 = *puVar15;
          puVar15 = (undefined4 *)
                    std::basic_string<char,std::char_traits<char>,std::allocator<char>_>::end
                              (local_c4);
          uVar22 = *puVar15;
          puVar15 = (undefined4 *)FUN_00684e50(local_234);
          FUN_00693eb0(*puVar15,uVar22,uVar5);
          local_1fc = (code *)&DAT_00c33d80;
          local_200 = 0;
          do {
            pcVar18 = local_1fc;
            FUN_0041e420(local_34,0x20,"%d.%d",*(int *)local_1fc,*(int *)(local_1fc + 4));
            FUN_0040c340(local_34);
            local_8._0_1_ = 10;
            FUN_00417910();
            iVar17 = FUN_00694fb0(*(int *)pcVar18,*(int *)(pcVar18 + 4),0);
            FUN_0040c340("unknown");
            local_8._0_1_ = 0xb;
            if (iVar17 != 0) {
              uVar5 = FUN_00694d20(local_64 + 6,0);
              FUN_004215a0(uVar5);
              thunk_FUN_0040d040();
            }
            FUN_0040cf50(local_7c);
            local_8._0_1_ = 0xc;
            puVar15 = (undefined4 *)FUN_00684e50((int)&local_218 + 4);
            uVar5 = *puVar15;
            puVar15 = (undefined4 *)
                      std::basic_string<char,std::char_traits<char>,std::allocator<char>_>::end
                                (local_7c);
            uVar22 = *puVar15;
            puVar15 = (undefined4 *)FUN_00684e50(local_234);
            FUN_00693eb0(*puVar15,uVar22,uVar5);
            uVar22 = 0;
            uVar5 = FUN_004143f0(1);
            iVar17 = FUN_00693650(uVar5,uVar22);
            if ((iVar17 == 0) || (iVar17 = FUN_00693650(local_c4,0), iVar17 != -1)) {
              iVar17 = local_200 * 4;
              thunk_FUN_0040d040();
              thunk_FUN_0040d040();
              thunk_FUN_0040d040();
              pcVar18 = (code *)(&DAT_00c33d80 + iVar17);
              break;
            }
            thunk_FUN_0040d040();
            thunk_FUN_0040d040();
            local_8._0_1_ = 8;
            thunk_FUN_0040d040();
            local_200 = local_200 + 1;
            local_1fc = local_1fc + 0x10;
            pcVar18 = local_204;
          } while (local_200 < 0x3b);
          local_8._0_1_ = 0;
          thunk_FUN_0040d040();
        }
        else {
          local_74 = 0;
          local_70 = 0;
          local_6c = 0;
          local_68 = 1;
          FUN_009b92c0(0);
          FUN_005caa70(&local_74,1);
        }
      }
      if (pcVar18 == (code *)0x0) {
        FUN_0040c340("Failed to spawn delirious boss: unsupported ID or Variant.\n");
        local_8._0_1_ = 0xd;
      }
      else {
        FUN_00417860();
        FUN_009b92c0(0);
        FUN_005caa70(pcVar18,1);
        FUN_0040c340("Spawned delirious boss.\n");
        local_8._0_1_ = 0xe;
      }
      goto LAB_0068d95d;
    }
    FUN_004143f0(0);
    cVar2 = FUN_004561b0();
    if (cVar2 == '\0') {
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if (cVar2 != '\0') {
        uVar6 = FUN_00414410();
        if (uVar6 < 2) {
          FUN_0040c340("Cleared forced room.\n");
          local_8._0_1_ = 0x16;
          FUN_006929e0(local_94,0xffd3d3d3,0x96);
          thunk_FUN_0040d040();
          DAT_00bf9428 = 0xffffffff;
          DAT_00bf9424 = 1;
          DAT_00c71668 = 0;
          uVar6 = DAT_00c7166c;
        }
        else {
          FUN_004143f0(1);
          pcVar3 = (char *)FUN_004170e0(1);
          uVar6 = DAT_00c7166c;
          if (*pcVar3 == '.') {
            FUN_004143f0(1);
            pcVar3 = (char *)FUN_004170e0(0);
            local_1e5 = *pcVar3;
            if ((local_1e5 == 's') || (local_1e5 == 'x')) {
              FUN_004143f0(1);
              FUN_00651a90(local_ac,2,0xffffffff);
              local_8._0_1_ = 0x17;
              FUN_0067f580(0x2e);
              local_8._0_1_ = 0x18;
              FUN_004143f0(0);
              uVar5 = FUN_0082d100();
              local_8._0_1_ = 0x17;
              thunk_FUN_004147f0();
              iVar17 = 0;
              FUN_0067f580(0x2e);
              local_8._0_1_ = 0x19;
              uVar6 = FUN_00414410();
              if (1 < uVar6) {
                FUN_004143f0(1);
                iVar4 = FUN_0040c2e0();
                if (iVar4 != 0) {
                  FUN_004143f0(1);
                  pcVar3 = (char *)FUN_0040d0c0();
                  iVar17 = atoi(pcVar3);
                }
              }
              if (local_1e5 == 'x') {
                FUN_00424530();
                DAT_00bf9428 = FUN_00738470(0);
              }
              else {
                DAT_00bf9428 = 0;
              }
              DAT_00bf9424 = uVar5;
              DAT_00c71668 = iVar17;
              thunk_FUN_004147f0();
              local_8._0_1_ = 0;
              thunk_FUN_0040d040();
            }
            else if (local_1e5 == 'd') {
              FUN_004143f0(1);
              FUN_00651a90(local_64 + 6,2,0xffffffff);
              pcVar3 = (char *)FUN_0040d0c0();
              iVar17 = atoi(pcVar3);
              thunk_FUN_0040d040();
              FUN_00424530();
              DAT_00bf9428 = FUN_00738470(0);
              DAT_00bf9424 = 1;
              DAT_00c71668 = iVar17;
            }
            iVar17 = DAT_00c71668;
            FUN_00421790();
            uVar5 = FUN_008295c0();
            FUN_00421790();
            FUN_0082d000(local_64 + 6,DAT_00bf9428,0);
            local_8._0_1_ = 0x1a;
            uVar22 = FUN_0040d0c0();
            FUN_00693090(param_1,"Set forced room to %s, %s, %d.\n",uVar22,uVar5,iVar17);
            thunk_FUN_0040d040();
            uVar6 = DAT_00c7166c;
          }
        }
        goto LAB_0069249e;
      }
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if ((cVar2 != '\0') && (uVar6 = FUN_00414410(), 1 < uVar6)) {
        uVar5 = 0x2e;
        FUN_004143f0(1);
        FUN_0067f580(uVar5);
        local_8._0_1_ = 0x1b;
        iVar4 = 0;
        local_1fc = (code *)0x0;
        iVar17 = FUN_00414410();
        if (iVar17 != 0) {
          FUN_004143f0(0);
          pcVar3 = (char *)FUN_0040d0c0();
          iVar4 = atoi(pcVar3);
        }
        uVar6 = FUN_00414410();
        if (1 < uVar6) {
          FUN_004143f0(1);
          pcVar3 = (char *)FUN_0040d0c0();
          local_1fc = (code *)atoi(pcVar3);
        }
        FUN_00407480();
        uVar5 = FUN_006eef60();
        iVar17 = FUN_0081ecc0(uVar5);
        uVar6 = FUN_00414410();
        if (2 < uVar6) {
          FUN_004143f0(2);
          pcVar3 = (char *)FUN_0040d0c0();
          iVar17 = atoi(pcVar3);
          FUN_00407480();
          FUN_0081e930(iVar17,0,0);
        }
        FUN_00407480();
        FUN_00685d60(iVar17,iVar4,local_1fc);
        FUN_00407480();
        iVar4 = FUN_00436060(iVar17);
        if (iVar4 != 0) {
          FUN_00407480();
          piVar8 = (int *)FUN_00436060(iVar17);
          (**(code **)(*piVar8 + 4))();
        }
        thunk_FUN_004147f0();
        uVar6 = DAT_00c7166c;
        goto LAB_0069249e;
      }
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if ((cVar2 != '\0') && (iVar17 = FUN_00414410(), iVar17 == 2)) {
        uVar5 = 0;
        FUN_004143f0(1);
        FUN_004143f0(1);
        iVar17 = FUN_0040c2e0();
        pcVar3 = (char *)FUN_004170e0(iVar17 + -1);
        if (*pcVar3 == 'a') {
          FUN_004143f0(1);
          FUN_004143f0(1);
          iVar17 = FUN_0040c2e0();
          FUN_00684ee0(iVar17 + -1,1);
          uVar5 = 1;
        }
        else {
          FUN_004143f0(1);
          FUN_004143f0(1);
          iVar17 = FUN_0040c2e0();
          pcVar3 = (char *)FUN_004170e0(iVar17 + -1);
          if (*pcVar3 == 'b') {
            FUN_004143f0(1);
            FUN_004143f0(1);
            iVar17 = FUN_0040c2e0();
            FUN_00684ee0(iVar17 + -1,1);
            uVar5 = 2;
          }
          else {
            FUN_004143f0(1);
            FUN_004143f0(1);
            iVar17 = FUN_0040c2e0();
            pcVar3 = (char *)FUN_004170e0(iVar17 + -1);
            if (*pcVar3 == 'c') {
              FUN_004143f0(1);
              FUN_004143f0(1);
              iVar17 = FUN_0040c2e0();
              FUN_00684ee0(iVar17 + -1,1);
              uVar5 = 4;
            }
            else {
              FUN_004143f0(1);
              FUN_004143f0(1);
              iVar17 = FUN_0040c2e0();
              pcVar3 = (char *)FUN_004170e0(iVar17 + -1);
              if (*pcVar3 == 'd') {
                FUN_004143f0(1);
                FUN_004143f0(1);
                iVar17 = FUN_0040c2e0();
                FUN_00684ee0(iVar17 + -1,1);
                uVar5 = 5;
              }
            }
          }
        }
        FUN_004143f0(1);
        pcVar3 = (char *)FUN_0040d0c0();
        iVar17 = atoi(pcVar3);
        uVar6 = DAT_00c7166c;
        if (0xd < iVar17 - 1U) goto LAB_0069249e;
        FUN_00424530();
        FUN_007466d0(iVar17,uVar5);
        FUN_00424530();
        Level__Init(0);
        FUN_00424530();
        FUN_00738610();
        FUN_00417860();
        FUN_009bc000();
        FUN_0040c340("Changed stage.\n");
        local_8._0_1_ = 0x1c;
        goto LAB_0068d95d;
      }
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if ((cVar2 != '\0') && (iVar17 = FUN_00414410(), iVar17 == 2)) {
        FUN_004143f0(1);
        pcVar3 = (char *)FUN_0040d0c0();
        iVar17 = atoi(pcVar3);
        uVar19 = iVar17 - 1;
        if (uVar19 < 0xe) {
          FUN_00685f10(uVar19);
          cVar2 = FUN_00431760(uVar19);
          if (cVar2 == '\0') {
            FUN_0040c340("Disabled debug flag.\n");
            local_8._0_1_ = 0x1e;
            FUN_006929e0(local_ac,0xffd3d3d3,0x96);
          }
          else {
            FUN_0040c340("Enabled debug flag.\n");
            local_8._0_1_ = 0x1d;
            FUN_006929e0(local_94,0xffd3d3d3,0x96);
          }
          local_8._0_1_ = 0;
          thunk_FUN_0040d040();
        }
        if (uVar19 == 8) {
          uVar19 = 0;
          iVar17 = FUN_004178d0();
          uVar6 = DAT_00c7166c;
          if (iVar17 != 0) {
            do {
              PlayerManager__get_player_417870(uVar19);
              FUN_007c2e80();
              uVar19 = uVar19 + 1;
              uVar9 = FUN_004178d0();
              uVar6 = DAT_00c7166c;
            } while (uVar19 < uVar9);
          }
        }
        else {
          uVar6 = DAT_00c7166c;
          if (uVar19 == 3) {
            uVar19 = 0;
            iVar17 = FUN_004178d0();
            uVar6 = DAT_00c7166c;
            if (iVar17 != 0) {
              do {
                PlayerManager__get_player_417870(uVar19);
                FUN_00436160(1);
                PlayerManager__get_player_417870(uVar19);
                FUN_00763570();
                uVar19 = uVar19 + 1;
                uVar9 = FUN_004178d0();
                uVar6 = DAT_00c7166c;
              } while (uVar19 < uVar9);
            }
          }
        }
        goto LAB_0069249e;
      }
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if (cVar2 != '\0') {
LAB_0068e5e5:
        uVar6 = FUN_00414410();
        if (uVar6 < 2) goto LAB_0068ef7a;
        FUN_004143f0(0);
        cVar2 = FUN_004561b0();
        if (cVar2 == '\0') {
          FUN_004143f0(0);
          cVar2 = FUN_004561b0();
          if (cVar2 != '\0') goto LAB_0068e674;
          FUN_004143f0(0);
          cVar2 = FUN_004561b0();
          if (cVar2 != '\0') goto LAB_0068e674;
          FUN_004143f0(0);
          cVar2 = FUN_004561b0();
          local_1f5 = '\0';
          if (cVar2 != '\0') goto LAB_0068e674;
        }
        else {
LAB_0068e674:
          local_1f5 = '\x01';
        }
        FUN_004143f0(0);
        FUN_00693680();
        FUN_004143f0(1);
        pcVar3 = (char *)FUN_0040d0c0();
        local_1e5 = *pcVar3;
        FUN_004143f0(0);
        pcVar10 = (char *)FUN_00693680();
        if ((*pcVar10 == '2') && (iVar17 = FUN_00417820(), iVar17 != 0)) {
          local_208 = FUN_00417820();
        }
        if ((byte)(pcVar3[1] - 0x30U) < 10) {
          local_20c = (int *)atoi(pcVar3 + 1);
        }
        else {
          local_20c = (int *)0xffffffff;
        }
        piVar8 = local_20c;
        if (local_1e5 != '*') {
          if (local_1e5 == 'c') {
            if (local_20c != (int *)0x0) {
              FUN_0042ca00();
              FUN_00424530();
              piVar11 = (int *)FUN_00417840();
              if (piVar8 < piVar11) {
                FUN_0042ca00();
                piVar11 = (int *)FUN_0072fd10(piVar8);
                uVar6 = DAT_00c7166c;
                if (piVar11 != (int *)0x0) {
                  if (local_1f5 == '\0') {
                    iVar17 = FUN_00421770();
                    if (iVar17 == 0x2b) {
                      FUN_007d8240(piVar8);
                      uVar6 = DAT_00c7166c;
                    }
                    else {
                      iVar17 = FUN_0042a2f0(0);
                      if ((iVar17 != 0) &&
                         (((cVar2 = FUN_007706e0(0x216,0), cVar2 == '\0' ||
                           (iVar17 = FUN_0042a2f0(1), iVar17 != 0)) && (*piVar11 == 3)))) {
                        FUN_0042ca00();
                        uVar5 = FUN_0042a2f0(0);
                        piVar11 = (int *)FUN_0072fd10(uVar5);
                        piVar8 = local_20c;
                        if ((piVar11 != (int *)0x0) && (*piVar11 == 3)) {
                          uVar23 = 1;
                          uVar21 = 0;
                          uVar22 = 0;
                          uVar5 = FUN_0042a2f0(0);
                          FUN_0078f840(uVar5,uVar22,uVar21,uVar23);
                          piVar8 = local_20c;
                        }
                      }
                      FUN_0075f0e0(piVar8,0xffffffff,1,0,0,0);
                      uVar6 = DAT_00c7166c;
                    }
                  }
                  else {
                    FUN_0078f840(piVar8,0,0,1);
                    uVar6 = DAT_00c7166c;
                  }
                }
                goto LAB_0069249e;
              }
            }
            goto LAB_0068e806;
          }
          if (((local_1e5 == 't') || (local_1e5 == 'T')) && (local_20c != (int *)0x0)) {
            FUN_0042ca00();
            FUN_00685d30();
            piVar11 = (int *)FUN_00417840();
            if (piVar8 < piVar11) {
              FUN_0042ca00();
              iVar17 = FUN_0072fd70(piVar8);
              uVar6 = DAT_00c7166c;
              if (iVar17 != 0) {
                if (local_1f5 == '\0') {
                  iVar17 = FUN_007717c0();
                  iVar17 = FUN_007a6430(iVar17 + -1);
                  if (iVar17 != 0) {
                    uVar5 = FUN_007a6430(0);
                    FUN_00771f60(uVar5);
                  }
                  if (local_1e5 == 'T') {
                    piVar8 = (int *)((uint)piVar8 | 0x8000);
                  }
                  FUN_00771d30(piVar8,1);
                  uVar6 = DAT_00c7166c;
                }
                else {
                  FUN_00771f60(piVar8);
                  uVar6 = DAT_00c7166c;
                }
              }
              goto LAB_0069249e;
            }
          }
          if (local_1e5 != 'k') {
            if ((local_1e5 == 'p') || (local_1e5 == 'P')) {
              FUN_0042ca00();
              FUN_0041e460();
              piVar11 = (int *)FUN_00417840();
              if (piVar8 < piVar11) {
                if (local_1f5 == '\0') {
                  FUN_0042a330();
                  uVar6 = FUN_00736ba0(piVar8);
                  if (local_1e5 == 'P') {
                    uVar6 = uVar6 | 0x800;
                  }
                  FUN_007a3c30(uVar6);
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                FUN_0040c340("Removing pills has not been implemented.\n");
                local_8._0_1_ = 0x22;
                goto LAB_0068d95d;
              }
            }
            goto LAB_0068e806;
          }
          if (piVar8 == (int *)0x0) goto LAB_0068e806;
          FUN_0042ca00();
          FUN_00685d40();
          piVar11 = (int *)FUN_00417840();
          if (piVar11 <= piVar8) goto LAB_0068e806;
          if (local_1f5 == '\0') {
            FUN_007a3c10(piVar8);
            uVar6 = DAT_00c7166c;
            goto LAB_0069249e;
          }
          FUN_0040c340("Removing cards has not been implemented.\n");
          local_8._0_1_ = 0x21;
          goto LAB_0068d95d;
        }
        if (local_1f5 == '\0') {
          FUN_0040c340("What are you trying to do?\n");
          local_8._0_1_ = 0x20;
          FUN_006929e0(local_94,0xffd3d3d3,0x96);
          local_8._0_1_ = 0;
          thunk_FUN_0040d040();
        }
        else {
          FUN_0040c340("Restoring player to zero collectibles/trinkets.\n");
          local_8._0_1_ = 0x1f;
          FUN_006929e0(local_94,0xffd3d3d3,0x96);
          local_8._0_1_ = 0;
          thunk_FUN_0040d040();
          uVar19 = 1;
          FUN_0042ca00();
          FUN_00424530();
          uVar6 = FUN_00417840();
          if (1 < uVar6) {
            do {
              cVar2 = FUN_0072fe30(uVar19);
              if (cVar2 != '\0') {
                FUN_0078f840(uVar19,0,0,1);
              }
              uVar19 = uVar19 + 1;
              FUN_0042ca00();
              FUN_00424530();
              uVar6 = FUN_00417840();
            } while (uVar19 < uVar6);
          }
          uVar19 = 1;
          FUN_0042ca00();
          FUN_00685d30();
          uVar6 = FUN_00417840();
          if (1 < uVar6) {
            do {
              FUN_00771f60(uVar19);
              uVar19 = uVar19 + 1;
              FUN_0042ca00();
              FUN_00685d30();
              uVar6 = FUN_00417840();
            } while (uVar19 < uVar6);
          }
        }
LAB_0068e806:
        uVar5 = FUN_004143f0(1);
        FUN_0040cf50(uVar5);
        local_8._0_1_ = 0x23;
        uVar6 = FUN_00414410();
        if (2 < uVar6) {
          uVar19 = 2;
          uVar6 = FUN_00414410();
          if (2 < uVar6) {
            do {
              uVar5 = FUN_004143f0(uVar19);
              FUN_00421620(&DAT_00b656ec);
              local_8._0_1_ = 0x24;
              uVar5 = FUN_00651d50(uVar5);
              FUN_004215a0(uVar5);
              thunk_FUN_0040d040();
              local_8._0_1_ = 0x23;
              thunk_FUN_0040d040();
              uVar19 = uVar19 + 1;
              uVar6 = FUN_00414410();
            } while (uVar19 < uVar6);
          }
        }
        puVar15 = (undefined4 *)FUN_00684e50((int)&local_218 + 4);
        uVar5 = *puVar15;
        puVar15 = (undefined4 *)
                  std::basic_string<char,std::char_traits<char>,std::allocator<char>_>::end
                            (local_7c);
        uVar22 = *puVar15;
        puVar15 = (undefined4 *)FUN_00684e50(local_234);
        FUN_00693eb0(*puVar15,uVar22,uVar5);
        local_1e5 = ' ';
        local_20d = 0x5f;
        puVar15 = (undefined4 *)
                  std::basic_string<char,std::char_traits<char>,std::allocator<char>_>::end
                            (local_7c);
        uVar5 = *puVar15;
        puVar15 = (undefined4 *)FUN_00684e50((int)&local_218 + 4);
        FUN_006851c0(*puVar15,uVar5);
        uVar6 = 0;
        FUN_0042ca00();
        FUN_00424530();
        iVar17 = FUN_00417840();
        if (iVar17 != 0) {
          do {
            FUN_0042ca00();
            iVar17 = FUN_0072fd10(uVar6);
            if (iVar17 != 0) {
              FUN_0072ff10(local_c4,0);
              local_8._0_1_ = 0x25;
              puVar15 = (undefined4 *)FUN_00684e50(local_224);
              uVar5 = *puVar15;
              puVar15 = (undefined4 *)
                        std::basic_string<char,std::char_traits<char>,std::allocator<char>_>::end
                                  (local_c4);
              uVar22 = *puVar15;
              puVar15 = (undefined4 *)FUN_00684e50(local_220);
              FUN_00693eb0(*puVar15,uVar22,uVar5);
              iVar17 = FUN_00693650(local_7c,0);
              if (iVar17 != -1) {
                if (local_1f5 == '\0') {
                  iVar17 = FUN_00421770();
                  if (iVar17 == 0x2b) {
                    FUN_007d8240(uVar6);
                    thunk_FUN_0040d040();
                    thunk_FUN_0040d040();
                    uVar6 = DAT_00c7166c;
                  }
                  else {
                    iVar17 = FUN_0042a2f0(0);
                    if ((iVar17 != 0) &&
                       ((cVar2 = FUN_007706e0(0x216,0), cVar2 == '\0' ||
                        (iVar17 = FUN_0042a2f0(1), iVar17 != 0)))) {
                      FUN_0042ca00();
                      piVar8 = (int *)FUN_0072fd10(uVar6);
                      if (*piVar8 == 3) {
                        FUN_0042ca00();
                        uVar5 = FUN_0042a2f0(0);
                        piVar8 = (int *)FUN_0072fd10(uVar5);
                        if ((piVar8 != (int *)0x0) && (*piVar8 == 3)) {
                          uVar23 = 1;
                          uVar21 = 0;
                          uVar22 = 0;
                          uVar5 = FUN_0042a2f0(0);
                          FUN_0078f840(uVar5,uVar22,uVar21,uVar23);
                        }
                      }
                    }
                    FUN_0075f0e0(uVar6,0xffffffff,1,0,0,0);
                    thunk_FUN_0040d040();
                    thunk_FUN_0040d040();
                    uVar6 = DAT_00c7166c;
                  }
                }
                else {
                  FUN_0078f840(uVar6,0,0,1);
                  thunk_FUN_0040d040();
                  thunk_FUN_0040d040();
                  uVar6 = DAT_00c7166c;
                }
                goto LAB_0069249e;
              }
              local_8._0_1_ = 0x23;
              thunk_FUN_0040d040();
            }
            uVar6 = uVar6 + 1;
            FUN_0042ca00();
            FUN_00424530();
            uVar19 = FUN_00417840();
          } while (uVar6 < uVar19);
        }
        uVar6 = 0;
        FUN_0042ca00();
        FUN_00685d30();
        iVar17 = FUN_00417840();
        if (iVar17 != 0) {
          do {
            FUN_0042ca00();
            iVar17 = FUN_0072fd70(uVar6);
            if (iVar17 != 0) {
              FUN_0072ff10(local_ac,0);
              local_8._0_1_ = 0x26;
              puVar15 = (undefined4 *)FUN_00684e50((int)&local_218 + 4);
              uVar5 = *puVar15;
              puVar15 = (undefined4 *)
                        std::basic_string<char,std::char_traits<char>,std::allocator<char>_>::end
                                  (local_ac);
              uVar22 = *puVar15;
              puVar15 = (undefined4 *)FUN_00684e50(local_234);
              FUN_00693eb0(*puVar15,uVar22,uVar5);
              iVar17 = FUN_00693650(local_7c,0);
              if (iVar17 != -1) {
                if (local_1f5 != '\0') {
                  FUN_00771f60(uVar6);
                  thunk_FUN_0040d040();
                  thunk_FUN_0040d040();
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                iVar17 = FUN_007717c0();
                iVar17 = FUN_007a6430(iVar17 + -1);
                if (iVar17 != 0) {
                  uVar5 = FUN_007a6430(0);
                  FUN_00771f60(uVar5);
                }
                FUN_00771d30(uVar6,1);
                thunk_FUN_0040d040();
                goto LAB_0068ef6d;
              }
              local_8._0_1_ = 0x23;
              thunk_FUN_0040d040();
            }
            uVar6 = uVar6 + 1;
            FUN_0042ca00();
            FUN_00685d30();
            uVar19 = FUN_00417840();
          } while (uVar6 < uVar19);
          thunk_FUN_0040d040();
          uVar6 = DAT_00c7166c;
          goto LAB_0069249e;
        }
LAB_0068ef6d:
        thunk_FUN_0040d040();
        uVar6 = DAT_00c7166c;
        goto LAB_0069249e;
      }
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if (cVar2 != '\0') goto LAB_0068e5e5;
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if (cVar2 != '\0') goto LAB_0068e5e5;
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if (cVar2 != '\0') goto LAB_0068e5e5;
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if (cVar2 != '\0') goto LAB_0068e5e5;
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if (cVar2 != '\0') goto LAB_0068e5e5;
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if (cVar2 != '\0') goto LAB_0068e5e5;
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if (cVar2 != '\0') goto LAB_0068e5e5;
LAB_0068ef7a:
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if ((cVar2 != '\0') && (iVar17 = FUN_00414410(), iVar17 == 2)) {
        FUN_004143f0(1);
        pcVar3 = (char *)FUN_0040d0c0();
        cVar2 = *pcVar3;
        if ((byte)(pcVar3[1] - 0x30U) < 10) {
          uVar6 = atoi(pcVar3 + 1);
        }
        else {
          uVar6 = 0xffffffff;
        }
        if (cVar2 == 'c') {
          FUN_0042ca00();
          FUN_00424530();
          uVar19 = FUN_00417840();
          if (uVar6 < uVar19) goto LAB_0069249e;
        }
        uVar5 = FUN_004143f0(1);
        FUN_0040cf50(uVar5);
        local_8._0_1_ = 0x27;
        uVar6 = FUN_00414410();
        if (2 < uVar6) {
          uVar19 = 2;
          uVar6 = FUN_00414410();
          if (2 < uVar6) {
            do {
              uVar5 = FUN_004143f0(uVar19);
              FUN_00421620(&DAT_00b656ec);
              local_8._0_1_ = 0x28;
              uVar5 = FUN_00651d50(uVar5);
              FUN_004215a0(uVar5);
              thunk_FUN_0040d040();
              local_8._0_1_ = 0x27;
              thunk_FUN_0040d040();
              uVar19 = uVar19 + 1;
              uVar6 = FUN_00414410();
            } while (uVar19 < uVar6);
          }
        }
        puVar15 = (undefined4 *)FUN_00684e50((int)&local_218 + 4);
        uVar5 = *puVar15;
        puVar15 = (undefined4 *)
                  std::basic_string<char,std::char_traits<char>,std::allocator<char>_>::end
                            (local_7c);
        uVar22 = *puVar15;
        puVar15 = (undefined4 *)FUN_00684e50(local_234);
        FUN_00693eb0(*puVar15,uVar22,uVar5);
        local_20d = 0x20;
        local_1e5 = '_';
        puVar15 = (undefined4 *)
                  std::basic_string<char,std::char_traits<char>,std::allocator<char>_>::end
                            (local_7c);
        uVar5 = *puVar15;
        puVar15 = (undefined4 *)FUN_00684e50((int)&local_218 + 4);
        FUN_006851c0(*puVar15,uVar5);
        uVar6 = 0;
        FUN_0042ca00();
        FUN_00424530();
        iVar17 = FUN_00417840();
        if (iVar17 != 0) {
          do {
            FUN_0042ca00();
            iVar17 = FUN_0072fd10(uVar6);
            if (iVar17 != 0) {
              FUN_0072ff10(local_ac,0);
              local_8._0_1_ = 0x29;
              puVar15 = (undefined4 *)FUN_00684e50(local_224);
              uVar5 = *puVar15;
              puVar15 = (undefined4 *)
                        std::basic_string<char,std::char_traits<char>,std::allocator<char>_>::end
                                  (local_ac);
              uVar22 = *puVar15;
              puVar15 = (undefined4 *)FUN_00684e50(local_220);
              FUN_00693eb0(*puVar15,uVar22,uVar5);
              iVar17 = FUN_00693650(local_7c,0);
              if (iVar17 != -1) {
                DAT_00c7166c = uVar6;
                thunk_FUN_0040d040();
                thunk_FUN_0040d040();
                uVar6 = DAT_00c7166c;
                goto LAB_0069249e;
              }
              local_8._0_1_ = 0x27;
              thunk_FUN_0040d040();
            }
            uVar6 = uVar6 + 1;
            FUN_0042ca00();
            FUN_00424530();
            uVar19 = FUN_00417840();
          } while (uVar6 < uVar19);
          thunk_FUN_0040d040();
          uVar6 = DAT_00c7166c;
          goto LAB_0069249e;
        }
        goto LAB_0068ef6d;
      }
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if (cVar2 != '\0') {
        iVar17 = FUN_0067f010();
        pcVar18 = (code *)(iVar17 + 2);
        local_1fc = pcVar18;
        iVar17 = FUN_00414410();
        if (iVar17 == 2) {
          FUN_004143f0(1);
          pcVar3 = (char *)FUN_0040d0c0();
          pcVar18 = (code *)atoi(pcVar3);
          local_1fc = pcVar18;
        }
        FUN_0075dfe0();
        if (0 < (int)pcVar18) {
          iVar17 = 0;
          do {
            do {
              do {
                uVar5 = FUN_0067f010();
                FUN_0042ca00();
                piVar8 = (int *)FUN_0072fd10(uVar5);
              } while (piVar8 == (int *)0x0);
            } while (*piVar8 != 1);
            FUN_0075d1d0(piVar8,0);
            iVar17 = iVar17 + 1;
            param_1 = local_20c;
            pcVar18 = local_1fc;
          } while (iVar17 < (int)local_1fc);
        }
        pcVar3 = "%d random costumes added.\n";
        goto LAB_00692495;
      }
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if (cVar2 != '\0') {
        iVar17 = FUN_00685f00();
        FUN_00693090(local_20c,"Total time: %02d:%02d.%02d\n",(iVar17 / 0x1e) / 0x3c,
                     (iVar17 / 0x1e) % 0x3c,((iVar17 % 0x1e) * 100) / 0x1e);
        uVar6 = DAT_00c7166c;
        goto LAB_0069249e;
      }
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if (cVar2 != '\0') {
        iVar17 = FUN_00414410();
        if (iVar17 == 2) {
          FUN_004143f0(1);
          iVar17 = FUN_0040c2e0();
          if (iVar17 != 0) {
            FUN_004143f0(1);
            pcVar3 = (char *)FUN_0040d0c0();
            iVar17 = atoi(pcVar3);
            if (iVar17 < 0) {
LAB_0068f438:
              iVar17 = 0;
            }
            else {
              FUN_00417910();
              FUN_00685d50();
              iVar4 = FUN_00693540();
              if (iVar4 <= iVar17) goto LAB_0068f438;
            }
            *(int *)(DAT_00c7169c + 0x4b134) = iVar17;
          }
        }
        uVar21 = 0;
        uVar22 = 0;
        uVar5 = FUN_0042a340();
        FUN_009e9320(uVar5);
        FUN_00958cb0(in_stack_fffffd40,in_stack_fffffd44,in_stack_fffffd48,in_stack_fffffd4c,
                     in_stack_fffffd50,in_stack_fffffd54,in_stack_fffffd58,in_stack_fffffd5c,
                     in_stack_fffffd60,in_stack_fffffd64,in_stack_fffffd68,in_stack_fffffd6c,
                     in_stack_fffffd70,in_stack_fffffd74,in_stack_fffffd78,in_stack_fffffd7c,
                     in_stack_fffffd80,in_stack_fffffd84,in_stack_fffffd88,in_stack_fffffd8c,
                     in_stack_fffffd90,in_stack_fffffd94,in_stack_fffffd98,uVar22,uVar21);
        uVar6 = DAT_00c7166c;
        goto LAB_0069249e;
      }
      FUN_004143f0(0);
      cVar2 = FUN_004561b0();
      if (cVar2 == '\0') {
        FUN_004143f0(0);
        cVar2 = FUN_004561b0();
        if ((cVar2 == '\0') || (iVar17 = FUN_00414410(), iVar17 != 2)) {
          FUN_004143f0(0);
          cVar2 = FUN_004561b0();
          if (cVar2 != '\0') {
            uVar6 = FUN_00414410();
            if (uVar6 < 2) {
              FUN_0042a340();
              FUN_00685dc0(local_ac);
              local_8._0_1_ = 0x35;
              FUN_006929e0(local_ac,0xffd3d3d3,0x96);
              FUN_0040c340(&DAT_00b66310);
              local_8._0_1_ = 0x36;
              FUN_006929e0(local_94,0xffd3d3d3,0x96);
              thunk_FUN_0040d040();
              thunk_FUN_0040d040();
              uVar6 = DAT_00c7166c;
            }
            else {
              uVar5 = FUN_004143f0(1);
              FUN_0040cf50(uVar5);
              local_8._0_1_ = 0x2f;
              uVar6 = FUN_00414410();
              if (2 < uVar6) {
                uVar5 = FUN_004143f0(2);
                uVar22 = 0x20;
                FUN_004143f0(1);
                FUN_00694170(uVar22);
                local_8._0_1_ = 0x30;
                in_stack_fffffd98 = 0x68f7e0;
                uVar5 = FUN_00651d50(uVar5);
                FUN_004215a0(uVar5);
                thunk_FUN_0040d040();
                local_8._0_1_ = 0x2f;
                thunk_FUN_0040d040();
              }
              cVar2 = Seeds__IsStringValidSeed(local_7c);
              if (cVar2 == '\0') {
                FUN_0040c340("Invalid seed.\n");
                local_8._0_1_ = 0x34;
              }
              else {
                FUN_0042a340();
                uVar5 = 0x68f828;
                cVar2 = FUN_00685ea0(local_7c);
                if (cVar2 == '\0') {
                  uVar23 = 0x68f83a;
                  FUN_0042a340();
                  uVar22 = 0x68f84a;
                  FUN_0040cf50(local_7c);
                  uVar21 = 0x68f851;
                  FUN_009eb7f0(in_stack_fffffd8c,in_stack_fffffd90,in_stack_fffffd94,
                               in_stack_fffffd98,uVar5,uVar23);
                  FUN_0042a340();
                  FUN_00685db0(1);
                  uVar24 = 0;
                  uVar23 = 0;
                  uVar5 = FUN_0042a340();
                  FUN_009e9320(uVar5);
                  FUN_00958cb0(in_stack_fffffd40,in_stack_fffffd44,in_stack_fffffd48,
                               in_stack_fffffd4c,in_stack_fffffd50,in_stack_fffffd54,
                               in_stack_fffffd58,in_stack_fffffd5c,in_stack_fffffd60,
                               in_stack_fffffd64,in_stack_fffffd68,in_stack_fffffd6c,
                               in_stack_fffffd70,in_stack_fffffd74,in_stack_fffffd78,
                               in_stack_fffffd7c,in_stack_fffffd80,uVar22,uVar21,in_stack_fffffd8c,
                               in_stack_fffffd90,in_stack_fffffd94,in_stack_fffffd98,uVar23,uVar24);
                  thunk_FUN_0040d040();
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                FUN_0042a340();
                cVar2 = FUN_009e9d10(local_7c);
                if (cVar2 == '\0') {
                  FUN_0042a340();
                  cVar2 = FUN_00685e00(local_7c);
                  if (cVar2 == '\0') {
                    FUN_0040c340("Special seed conflicts with the current stack.\n");
                    local_8._0_1_ = 0x32;
                  }
                  else {
                    FUN_0042a340();
                    FUN_009eba40(local_7c);
                    FUN_0040c340("Removed special seed.\n");
                    local_8._0_1_ = 0x31;
                  }
                }
                else {
                  FUN_0042a340();
                  FUN_009eba00(local_7c);
                  FUN_0040c340("Added special seed.\n");
                  local_8._0_1_ = 0x33;
                }
              }
              FUN_006929e0(local_94,0xffd3d3d3,0x96);
              thunk_FUN_0040d040();
              thunk_FUN_0040d040();
              uVar6 = DAT_00c7166c;
            }
            goto LAB_0069249e;
          }
          FUN_004143f0(0);
          cVar2 = FUN_004561b0();
          if (cVar2 != '\0') {
            FUN_0042a340();
            FUN_00685e70();
            uVar6 = DAT_00c7166c;
            goto LAB_0069249e;
          }
          FUN_004143f0(0);
          cVar2 = FUN_004561b0();
          if (cVar2 != '\0') {
            iVar17 = FUN_00414410();
            if (iVar17 == 2) {
              FUN_004143f0(1);
              iVar17 = FUN_0040c2e0();
              if (iVar17 != 0) {
                FUN_004143f0(1);
                pcVar3 = (char *)FUN_0040d0c0();
                uVar6 = atoi(pcVar3);
                if ((-1 < (int)uVar6) && (uVar19 = FUN_00685f70(), uVar6 <= uVar19)) {
                  iVar4 = FUN_009569a0(uVar6);
                  iVar17 = DAT_00c7169c;
                  uVar21 = 0;
                  uVar22 = 0;
                  *(uint *)(DAT_00c7169c + 0x4b138) = uVar6;
                  *(undefined4 *)(iVar17 + 0x4b134) = *(undefined4 *)(iVar4 + 0x44);
                  *(undefined4 *)(iVar17 + 0x4b198) = *(undefined4 *)(iVar4 + 0x70);
                  uVar5 = FUN_0042a340();
                  FUN_009e9320(uVar5);
                  FUN_00958cb0(in_stack_fffffd40,in_stack_fffffd44,in_stack_fffffd48,
                               in_stack_fffffd4c,in_stack_fffffd50,in_stack_fffffd54,
                               in_stack_fffffd58,in_stack_fffffd5c,in_stack_fffffd60,
                               in_stack_fffffd64,in_stack_fffffd68,in_stack_fffffd6c,
                               in_stack_fffffd70,in_stack_fffffd74,in_stack_fffffd78,
                               in_stack_fffffd7c,in_stack_fffffd80,in_stack_fffffd84,
                               in_stack_fffffd88,in_stack_fffffd8c,in_stack_fffffd90,
                               in_stack_fffffd94,in_stack_fffffd98,uVar22,uVar21);
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                FUN_0040c340("Invalid challenge ID.\n");
                local_8._0_1_ = 0x37;
                goto LAB_0068d95d;
              }
            }
            FUN_0040c340("Invalid challenge ID.\n");
            local_8._0_1_ = 0x38;
            goto LAB_0068d95d;
          }
          FUN_004143f0(0);
          cVar2 = FUN_004561b0();
          if ((cVar2 == '\0') || (iVar17 = FUN_00414410(), iVar17 != 2)) {
            FUN_004143f0(0);
            cVar2 = FUN_004561b0();
            if ((cVar2 == '\0') || (iVar17 = FUN_00414410(), iVar17 != 2)) {
              FUN_004143f0(0);
              cVar2 = FUN_004561b0();
              if (cVar2 == '\0') {
                FUN_004143f0(0);
                cVar2 = FUN_004561b0();
                if (cVar2 != '\0') {
                  FUN_0040e470();
                  FUN_0040e910();
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                FUN_004143f0(0);
                cVar2 = FUN_004561b0();
                if (cVar2 == '\0') {
                  FUN_004143f0(0);
                  cVar2 = FUN_004561b0();
                  if (cVar2 != '\0') goto LAB_0068fda9;
                }
                else {
LAB_0068fda9:
                  uVar6 = FUN_00414410();
                  if (1 < uVar6) {
                    FUN_004143f0(1);
                    cVar2 = FUN_004561b0();
                    if (cVar2 != '\0') {
                      FUN_006fe2f0(0xffffffec,0xffffffff);
                      uVar6 = DAT_00c7166c;
                      goto LAB_0069249e;
                    }
                    FUN_004143f0(1);
                    cVar2 = FUN_004561b0();
                    if (cVar2 == '\0') {
                      FUN_004143f0(1);
                      cVar2 = FUN_004561b0();
                      if (cVar2 == '\0') {
                        FUN_004143f0(1);
                        cVar2 = FUN_004561b0();
                        if (cVar2 != '\0') {
                          FUN_0040c340("goto s.boss.5000");
                          local_8._0_1_ = 0x43;
                          Game__boss_pool_state_loader(local_dc,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("giveitem Soy");
                          local_8._0_1_ = 0x44;
                          Game__boss_pool_state_loader(local_10c,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("giveitem Mutant");
                          local_8._0_1_ = 0x45;
                          Game__boss_pool_state_loader(local_94,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("debug 3");
                          local_8._0_1_ = 0x46;
                          Game__boss_pool_state_loader(local_ac,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("debug 4");
                          local_8._0_1_ = 0x47;
                          Game__boss_pool_state_loader(local_7c,0,0);
                          thunk_FUN_0040d040();
                          uVar6 = DAT_00c7166c;
                          goto LAB_0069249e;
                        }
                        FUN_004143f0(1);
                        cVar2 = FUN_004561b0();
                        if (cVar2 != '\0') {
                          FUN_0040c340("stage 11a");
                          local_8._0_1_ = 0x48;
                          Game__boss_pool_state_loader(local_dc,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("goto s.boss.6000");
                          local_8._0_1_ = 0x49;
LAB_00690100:
                          Game__boss_pool_state_loader(local_10c,0,0);
                          thunk_FUN_0040d040();
                          uVar6 = DAT_00c7166c;
                          goto LAB_0069249e;
                        }
                        FUN_004143f0(1);
                        cVar2 = FUN_004561b0();
                        if (cVar2 != '\0') {
                          FUN_0040c340("stage 11a");
                          local_8._0_1_ = 0x4a;
                          Game__boss_pool_state_loader(local_dc,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("goto s.boss.6000");
                          local_8._0_1_ = 0x4b;
                          Game__boss_pool_state_loader(local_10c,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("giveitem Sad Onion");
                          local_8._0_1_ = 0x4c;
                          Game__boss_pool_state_loader(local_94,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("giveitem Sad Onion");
                          local_8._0_1_ = 0x4d;
                          Game__boss_pool_state_loader(local_ac,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("giveitem Torn");
                          local_8._0_1_ = 0x4e;
                          Game__boss_pool_state_loader(local_7c,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("giveitem Torn");
                          local_8._0_1_ = 0x4f;
                          Game__boss_pool_state_loader(local_c4,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("giveitem Mutant");
                          local_8._0_1_ = 0x50;
                          Game__boss_pool_state_loader(local_154,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("giveitem A Dollar");
                          local_8._0_1_ = 0x51;
                          Game__boss_pool_state_loader(local_13c,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("giveitem Pyro");
                          local_8._0_1_ = 0x52;
                          Game__boss_pool_state_loader(local_124,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("debug 3");
                          local_8._0_1_ = 0x53;
                          Game__boss_pool_state_loader(local_f4,0,0);
                          thunk_FUN_0040d040();
                          uVar6 = DAT_00c7166c;
                          goto LAB_0069249e;
                        }
                        FUN_004143f0(1);
                        cVar2 = FUN_004561b0();
                        if (cVar2 == '\0') {
                          FUN_004143f0(1);
                          cVar2 = FUN_004561b0();
                          if (cVar2 == '\0') {
                            FUN_004143f0(1);
                            cVar2 = FUN_004561b0();
                            if (cVar2 != '\0') {
                              local_64[0] = "stage 10a";
                              uVar19 = 0;
                              local_64[1] = "g Polaroid";
                              local_64[2] = "g Negative";
                              local_64[3] = "debug 3";
                              local_64[4] = "debug 4";
                              local_64[5] = "g Mutant";
                              local_64[6] = "g Soy";
                              local_64[7] = "giveitem Belt";
                              local_64[8] = "repeat 5";
                              local_64[9] = "giveitem Lord of the Pit";
                              local_64[10] = "debug 10";
                              local_64[0xb] = "g k5";
                              do {
                                FUN_0040c340(local_64[uVar19]);
                                local_8._0_1_ = 0x5e;
                                Game__boss_pool_state_loader(local_f4,0,0);
                                local_8._0_1_ = 0;
                                thunk_FUN_0040d040();
                                uVar19 = uVar19 + 1;
                                uVar6 = DAT_00c7166c;
                              } while (uVar19 < 0xc);
                              goto LAB_0069249e;
                            }
                            FUN_004143f0(1);
                            cVar2 = FUN_004561b0();
                            if (cVar2 == '\0') {
                              FUN_004143f0(1);
                              cVar2 = FUN_004561b0();
                              if (cVar2 == '\0') {
                                FUN_004143f0(1);
                                cVar2 = FUN_004561b0();
                                if (cVar2 == '\0') {
                                  FUN_004143f0(1);
                                  cVar2 = FUN_004561b0();
                                  if (cVar2 == '\0') {
                                    FUN_004143f0(1);
                                    cVar2 = FUN_004561b0();
                                    if (cVar2 == '\0') {
                                      FUN_004143f0(1);
                                      cVar2 = FUN_004561b0();
                                      if (cVar2 == '\0') {
                                        FUN_004143f0(1);
                                        cVar2 = FUN_004561b0();
                                        if (cVar2 == '\0') {
                                          FUN_004143f0(1);
                                          cVar2 = FUN_004561b0();
                                          if (cVar2 == '\0') {
                                            FUN_004143f0(1);
                                            cVar2 = FUN_004561b0();
                                            if (cVar2 == '\0') {
                                              FUN_004143f0(1);
                                              cVar2 = FUN_004561b0();
                                              uVar6 = DAT_00c7166c;
                                              if ((cVar2 != '\0') &&
                                                 (uVar19 = FUN_00414410(), uVar6 = DAT_00c7166c,
                                                 2 < uVar19)) {
                                                uVar5 = FUN_004143f0(2);
                                                uVar5 = FUN_006941b0(uVar5);
                                                local_8._0_1_ = 0x9d;
                                                Game__boss_pool_state_loader(uVar5,0,0);
                                                thunk_FUN_0040d040();
                                                uVar6 = DAT_00c7166c;
                                              }
                                            }
                                            else {
                                              uVar19 = FUN_00414410();
                                              uVar6 = DAT_00c7166c;
                                              if (2 < uVar19) {
                                                uVar5 = FUN_004143f0(2);
                                                uVar5 = FUN_006941b0(uVar5);
                                                local_8._0_1_ = 0x9c;
                                                Game__boss_pool_state_loader(uVar5,0,0);
                                                thunk_FUN_0040d040();
                                                uVar6 = DAT_00c7166c;
                                              }
                                            }
                                          }
                                          else {
                                            uVar19 = FUN_00414410();
                                            uVar6 = DAT_00c7166c;
                                            if (3 < uVar19) {
                                              uVar5 = FUN_004143f0(2);
                                              uVar5 = FUN_006941b0(uVar5);
                                              local_8._0_1_ = 0x9a;
                                              Game__boss_pool_state_loader(uVar5,0,0);
                                              local_8._0_1_ = 0;
                                              thunk_FUN_0040d040();
                                              uVar5 = FUN_004143f0(3);
                                              uVar5 = FUN_006941b0(uVar5);
                                              local_8._0_1_ = 0x9b;
                                              Game__boss_pool_state_loader(uVar5,0,0);
                                              thunk_FUN_0040d040();
                                              uVar6 = DAT_00c7166c;
                                            }
                                          }
                                        }
                                        else {
                                          FUN_0040c340("debug 16");
                                          local_8._0_1_ = 0x98;
                                          Game__boss_pool_state_loader(local_64 + 6,0,0);
                                          local_8._0_1_ = 0;
                                          thunk_FUN_0040d040();
                                          FUN_0040c340("twitch_init");
                                          local_8._0_1_ = 0x99;
                                          Game__boss_pool_state_loader(local_2c,0,0);
                                          thunk_FUN_0040d040();
                                          uVar6 = DAT_00c7166c;
                                        }
                                      }
                                      else {
                                        FUN_0040c340("giveitem Belt");
                                        local_8._0_1_ = 0x92;
                                        Game__boss_pool_state_loader(local_64 + 6,0,0);
                                        local_8._0_1_ = 0;
                                        thunk_FUN_0040d040();
                                        FUN_0040c340("giveitem Lord of the Pit");
                                        local_8._0_1_ = 0x93;
                                        Game__boss_pool_state_loader(local_2c,0,0);
                                        local_8._0_1_ = 0;
                                        thunk_FUN_0040d040();
                                        FUN_0040c340("giveitem Treasure Map");
                                        local_8._0_1_ = 0x94;
                                        Game__boss_pool_state_loader(local_16c,0,0);
                                        local_8._0_1_ = 0;
                                        thunk_FUN_0040d040();
                                        FUN_0040c340("giveitem Blue Map");
                                        local_8._0_1_ = 0x95;
                                        Game__boss_pool_state_loader(local_19c,0,0);
                                        local_8._0_1_ = 0;
                                        thunk_FUN_0040d040();
                                        FUN_0040c340("giveitem Compass");
                                        local_8._0_1_ = 0x96;
                                        Game__boss_pool_state_loader(local_1b4,0,0);
                                        local_8._0_1_ = 0;
                                        thunk_FUN_0040d040();
                                        FUN_0040c340("debug 3");
                                        local_8._0_1_ = 0x97;
                                        Game__boss_pool_state_loader(local_1cc,0,0);
                                        thunk_FUN_0040d040();
                                        uVar6 = DAT_00c7166c;
                                      }
                                    }
                                    else {
                                      FUN_0040c340("giveitem Belt");
                                      local_8._0_1_ = 0x83;
                                      Game__boss_pool_state_loader(local_64 + 6,0,0);
                                      local_8._0_1_ = 0;
                                      thunk_FUN_0040d040();
                                      FUN_0040c340("repeat 5");
                                      local_8._0_1_ = 0x84;
                                      Game__boss_pool_state_loader(local_2c,0,0);
                                      local_8._0_1_ = 0;
                                      thunk_FUN_0040d040();
                                      FUN_0040c340("giveitem Lord of the Pit");
                                      local_8._0_1_ = 0x85;
                                      Game__boss_pool_state_loader(local_16c,0,0);
                                      local_8._0_1_ = 0;
                                      thunk_FUN_0040d040();
                                      FUN_0040c340("giveitem Treasure Map");
                                      local_8._0_1_ = 0x86;
                                      Game__boss_pool_state_loader(local_19c,0,0);
                                      local_8._0_1_ = 0;
                                      thunk_FUN_0040d040();
                                      FUN_0040c340("giveitem Blue Map");
                                      local_8._0_1_ = 0x87;
                                      Game__boss_pool_state_loader(local_1b4,0,0);
                                      local_8._0_1_ = 0;
                                      thunk_FUN_0040d040();
                                      FUN_0040c340("giveitem Compass");
                                      local_8._0_1_ = 0x88;
                                      Game__boss_pool_state_loader(local_1cc,0,0);
                                      local_8._0_1_ = 0;
                                      thunk_FUN_0040d040();
                                      FUN_0040c340("giveitem Black Candle");
                                      local_8._0_1_ = 0x89;
                                      Game__boss_pool_state_loader(local_1e4,0,0);
                                      local_8._0_1_ = 0;
                                      thunk_FUN_0040d040();
                                      FUN_0040c340("giveitem X-Ray");
                                      local_8._0_1_ = 0x8a;
                                      Game__boss_pool_state_loader(local_f4,0,0);
                                      local_8._0_1_ = 0;
                                      thunk_FUN_0040d040();
                                      FUN_0040c340("giveitem We Need to Go Deeper");
                                      local_8._0_1_ = 0x8b;
                                      Game__boss_pool_state_loader(local_124,0,0);
                                      local_8._0_1_ = 0;
                                      thunk_FUN_0040d040();
                                      FUN_0040c340("debug 8");
                                      local_8._0_1_ = 0x8c;
                                      Game__boss_pool_state_loader(local_13c,0,0);
                                      local_8._0_1_ = 0;
                                      thunk_FUN_0040d040();
                                      FUN_0040c340("giveitem Dollar");
                                      local_8._0_1_ = 0x8d;
                                      Game__boss_pool_state_loader(local_154,0,0);
                                      local_8._0_1_ = 0;
                                      thunk_FUN_0040d040();
                                      FUN_0040c340("giveitem Pyro");
                                      local_8._0_1_ = 0x8e;
                                      Game__boss_pool_state_loader(local_dc,0,0);
                                      local_8._0_1_ = 0;
                                      thunk_FUN_0040d040();
                                      FUN_0040c340("giveitem Skeleton Key");
                                      local_8._0_1_ = 0x8f;
                                      Game__boss_pool_state_loader(local_10c,0,0);
                                      local_8._0_1_ = 0;
                                      thunk_FUN_0040d040();
                                      FUN_0040c340("debug 3");
                                      local_8._0_1_ = 0x90;
                                      Game__boss_pool_state_loader(local_94,0,0);
                                      local_8._0_1_ = 0;
                                      thunk_FUN_0040d040();
                                      FUN_0040c340("debug 10");
                                      local_8._0_1_ = 0x91;
                                      Game__boss_pool_state_loader(local_ac,0,0);
                                      thunk_FUN_0040d040();
                                      uVar6 = DAT_00c7166c;
                                    }
                                  }
                                  else {
                                    FUN_0040c340("giveitem Dead Cat");
                                    local_8._0_1_ = 0x72;
                                    Game__boss_pool_state_loader(local_f4,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("repeat 2");
                                    local_8._0_1_ = 0x73;
                                    Game__boss_pool_state_loader(local_124,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("giveitem Guppy\'s Collar");
                                    local_8._0_1_ = 0x74;
                                    Game__boss_pool_state_loader(local_13c,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("giveitem Holy Mantle");
                                    local_8._0_1_ = 0x75;
                                    Game__boss_pool_state_loader(local_154,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("giveitem Schoolbag");
                                    local_8._0_1_ = 0x76;
                                    Game__boss_pool_state_loader(local_dc,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("giveitem MEAT!");
                                    local_8._0_1_ = 0x77;
                                    Game__boss_pool_state_loader(local_10c,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("repeat 12");
                                    local_8._0_1_ = 0x78;
                                    Game__boss_pool_state_loader(local_94,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("giveitem Compass");
                                    local_8._0_1_ = 0x79;
                                    Game__boss_pool_state_loader(local_ac,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("giveitem Blue Map");
                                    local_8._0_1_ = 0x7a;
                                    Game__boss_pool_state_loader(local_7c,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("giveitem Treasure Map");
                                    local_8._0_1_ = 0x7b;
                                    Game__boss_pool_state_loader(local_c4,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("giveitem Baggy");
                                    local_8._0_1_ = 0x7c;
                                    Game__boss_pool_state_loader(local_1e4,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("giveitem p2");
                                    local_8._0_1_ = 0x7d;
                                    Game__boss_pool_state_loader(local_1cc,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("giveitem p3");
                                    local_8._0_1_ = 0x7e;
                                    Game__boss_pool_state_loader(local_1b4,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("giveitem Purse");
                                    local_8._0_1_ = 0x7f;
                                    Game__boss_pool_state_loader(local_19c,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("giveitem Paper Clip");
                                    local_8._0_1_ = 0x80;
                                    Game__boss_pool_state_loader(local_16c,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("giveitem Petrified");
                                    local_8._0_1_ = 0x81;
                                    Game__boss_pool_state_loader(local_2c,0,0);
                                    local_8._0_1_ = 0;
                                    thunk_FUN_0040d040();
                                    FUN_0040c340("giveitem My Little Unicorn");
                                    local_8._0_1_ = 0x82;
                                    Game__boss_pool_state_loader(local_64 + 6,0,0);
                                    thunk_FUN_0040d040();
                                    uVar6 = DAT_00c7166c;
                                  }
                                }
                                else {
                                  FUN_0040c340("stage 13");
                                  local_8._0_1_ = 0x6b;
                                  Game__boss_pool_state_loader(local_f4,0,0);
                                  local_8._0_1_ = 0;
                                  thunk_FUN_0040d040();
                                  FUN_0040c340("goto x.itemdungeon.666");
                                  local_8._0_1_ = 0x6c;
                                  Game__boss_pool_state_loader(local_124,0,0);
                                  local_8._0_1_ = 0;
                                  thunk_FUN_0040d040();
                                  FUN_0040c340("combo 0.8");
                                  local_8._0_1_ = 0x6d;
                                  Game__boss_pool_state_loader(local_13c,0,0);
                                  local_8._0_1_ = 0;
                                  thunk_FUN_0040d040();
                                  FUN_0040c340("combo 2.8");
                                  local_8._0_1_ = 0x6e;
                                  Game__boss_pool_state_loader(local_154,0,0);
                                  local_8._0_1_ = 0;
                                  thunk_FUN_0040d040();
                                  FUN_0040c340("combo 1.3");
                                  local_8._0_1_ = 0x6f;
                                  Game__boss_pool_state_loader(local_dc,0,0);
                                  local_8._0_1_ = 0;
                                  thunk_FUN_0040d040();
                                  FUN_0040c340("combo 4.3");
                                  local_8._0_1_ = 0x70;
                                  Game__boss_pool_state_loader(local_10c,0,0);
                                  local_8._0_1_ = 0;
                                  thunk_FUN_0040d040();
                                  FUN_0040c340("debug 3");
                                  local_8._0_1_ = 0x71;
                                  Game__boss_pool_state_loader(local_94,0,0);
                                  thunk_FUN_0040d040();
                                  uVar6 = DAT_00c7166c;
                                }
                                goto LAB_0069249e;
                              }
                              FUN_0040c340("combo 0.12");
                              local_8._0_1_ = 0x65;
                              Game__boss_pool_state_loader(local_f4,0,0);
                              local_8._0_1_ = 0;
                              thunk_FUN_0040d040();
                              FUN_0040c340("combo 2.12");
                              local_8._0_1_ = 0x66;
                              Game__boss_pool_state_loader(local_124,0,0);
                              local_8._0_1_ = 0;
                              thunk_FUN_0040d040();
                              FUN_0040c340("combo 1.3");
                              local_8._0_1_ = 0x67;
                              Game__boss_pool_state_loader(local_13c,0,0);
                              local_8._0_1_ = 0;
                              thunk_FUN_0040d040();
                              FUN_0040c340("combo 4.3");
                              local_8._0_1_ = 0x68;
                              Game__boss_pool_state_loader(local_154,0,0);
                              local_8._0_1_ = 0;
                              thunk_FUN_0040d040();
                              FUN_0040c340("debug 3");
                              local_8._0_1_ = 0x69;
                              Game__boss_pool_state_loader(local_dc,0,0);
                              local_8._0_1_ = 0;
                              thunk_FUN_0040d040();
                              FUN_0040c340("goto s.boss.3414");
                              local_8._0_1_ = 0x6a;
                            }
                            else {
                              FUN_0040c340("stage 9");
                              local_8._0_1_ = 0x5f;
                              Game__boss_pool_state_loader(local_f4,0,0);
                              local_8._0_1_ = 0;
                              thunk_FUN_0040d040();
                              FUN_0040c340(&DAT_00b665bc);
                              local_8._0_1_ = 0x60;
                              Game__boss_pool_state_loader(local_124,0,0);
                              local_8._0_1_ = 0;
                              thunk_FUN_0040d040();
                              FUN_0040c340("combo 0.8");
                              local_8._0_1_ = 0x61;
                              Game__boss_pool_state_loader(local_13c,0,0);
                              local_8._0_1_ = 0;
                              thunk_FUN_0040d040();
                              FUN_0040c340("combo 2.8");
                              local_8._0_1_ = 0x62;
                              Game__boss_pool_state_loader(local_154,0,0);
                              local_8._0_1_ = 0;
                              thunk_FUN_0040d040();
                              FUN_0040c340("combo 1.3");
                              local_8._0_1_ = 99;
                              Game__boss_pool_state_loader(local_dc,0,0);
                              local_8._0_1_ = 0;
                              thunk_FUN_0040d040();
                              FUN_0040c340("combo 4.3");
                              local_8._0_1_ = 100;
                            }
                            goto LAB_00690100;
                          }
                          FUN_0040c340("stage 8");
                          local_8._0_1_ = 0x59;
                          Game__boss_pool_state_loader(local_f4,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("g Bible");
                          local_8._0_1_ = 0x5a;
                          Game__boss_pool_state_loader(local_124,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340(&DAT_00b665bc);
                          local_8._0_1_ = 0x5b;
                          Game__boss_pool_state_loader(local_13c,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("debug 3");
                          local_8._0_1_ = 0x5c;
                          Game__boss_pool_state_loader(local_154,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("debug 4");
                          local_8._0_1_ = 0x5d;
                        }
                        else {
                          FUN_0040c340("stage 6");
                          local_8._0_1_ = 0x54;
                          Game__boss_pool_state_loader(local_f4,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("g Bible");
                          local_8._0_1_ = 0x55;
                          Game__boss_pool_state_loader(local_124,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340(&DAT_00b665bc);
                          local_8._0_1_ = 0x56;
                          Game__boss_pool_state_loader(local_13c,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("debug 3");
                          local_8._0_1_ = 0x57;
                          Game__boss_pool_state_loader(local_154,0,0);
                          local_8._0_1_ = 0;
                          thunk_FUN_0040d040();
                          FUN_0040c340("debug 4");
                          local_8._0_1_ = 0x58;
                        }
                      }
                      else {
                        FUN_0040c340("goto s.boss.5000");
                        local_8._0_1_ = 0x42;
                      }
                    }
                    else {
                      FUN_0040c340("debug 3");
                      local_8._0_1_ = 0x3c;
                      Game__boss_pool_state_loader(local_94,0,0);
                      local_8._0_1_ = 0;
                      thunk_FUN_0040d040();
                      FUN_0040c340("debug 8");
                      local_8._0_1_ = 0x3d;
                      Game__boss_pool_state_loader(local_ac,0,0);
                      local_8._0_1_ = 0;
                      thunk_FUN_0040d040();
                      FUN_0040c340("debug 9");
                      local_8._0_1_ = 0x3e;
                      Game__boss_pool_state_loader(local_7c,0,0);
                      local_8._0_1_ = 0;
                      thunk_FUN_0040d040();
                      FUN_0040c340("giveitem Soy");
                      local_8._0_1_ = 0x3f;
                      Game__boss_pool_state_loader(local_c4,0,0);
                      local_8._0_1_ = 0;
                      thunk_FUN_0040d040();
                      FUN_0040c340("giveitem Bar");
                      local_8._0_1_ = 0x40;
                      Game__boss_pool_state_loader(local_10c,0,0);
                      local_8._0_1_ = 0;
                      thunk_FUN_0040d040();
                      FUN_0040c340("giveitem Pad");
                      local_8._0_1_ = 0x41;
                    }
                    Game__boss_pool_state_loader(local_dc,0,0);
                    thunk_FUN_0040d040();
                    uVar6 = DAT_00c7166c;
                    goto LAB_0069249e;
                  }
                }
                FUN_004143f0(0);
                cVar2 = FUN_004561b0();
                if ((cVar2 != '\0') && (uVar6 = FUN_00414410(), 1 < uVar6)) {
                  local_1fc = DAT_00baa454;
                  uVar6 = FUN_00414410();
                  if (2 < uVar6) {
                    FUN_004143f0(2);
                    pcVar3 = (char *)FUN_0040d0c0();
                    dVar20 = atof(pcVar3);
                    local_204 = (code *)(float)dVar20;
                    local_1fc = local_204;
                  }
                  FUN_004143f0(1);
                  pcVar3 = (char *)FUN_0040d0c0();
                  iVar17 = atoi(pcVar3);
                  FUN_009568e0(iVar17,2,0,local_1fc);
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                FUN_004143f0(0);
                cVar2 = FUN_004561b0();
                if ((cVar2 != '\0') && (uVar6 = FUN_00414410(), 1 < uVar6)) {
                  uVar9 = 0;
                  uVar6 = 1;
                  uVar19 = FUN_00414410();
                  if (1 < uVar19) {
                    do {
                      FUN_004143f0(uVar6);
                      pcVar3 = (char *)FUN_0040d0c0();
                      uVar19 = atoi(pcVar3);
                      uVar9 = uVar9 | uVar19;
                      uVar6 = uVar6 + 1;
                      uVar19 = FUN_00414410();
                    } while (uVar6 < uVar19);
                  }
                  FUN_00685f50(uVar9);
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                FUN_004143f0(0);
                cVar2 = FUN_004561b0();
                if (cVar2 != '\0') {
                  FUN_0042a340();
                  FUN_00424530();
                  uVar5 = FUN_004360f0();
                  Seeds__advance_stage_slot(uVar5);
                  FUN_00424530();
                  Level__Init(1);
                  FUN_00424530();
                  FUN_00738610();
                  FUN_00417860();
                  FUN_009bc000();
                  FUN_0040c340("Changed stage.\n");
                  local_8._0_1_ = 0x9e;
LAB_00691611:
                  FUN_006929e0(local_64 + 6,0xffd3d3d3,0x96);
                  thunk_FUN_0040d040();
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                FUN_004143f0(0);
                cVar2 = FUN_004561b0();
                if (cVar2 != '\0') {
                  iVar17 = 0;
                  do {
                    FUN_00421800();
                    FUN_0092b230(iVar17);
                    iVar17 = iVar17 + 1;
                  } while (iVar17 < 0x50);
                  FUN_0040c340("All easter eggs unlocked in main menu.\n");
                  local_8._0_1_ = 0x9f;
                  FUN_006929e0(local_64 + 6,0xffd3d3d3,0x96);
                  local_8._0_1_ = 0;
                  thunk_FUN_0040d040();
                  FUN_0040c340("On the easter eggs menu press Q+E+Tab\n");
                  local_8._0_1_ = 0xa0;
                  FUN_006929e0(local_2c,0xffd3d3d3,0x96);
                  local_8._0_1_ = 0;
                  thunk_FUN_0040d040();
                  FUN_0040c340("or LB+RB+X to remove one from the list.\n");
                  local_8._0_1_ = 0xa1;
                  FUN_006929e0(local_16c,0xffd3d3d3,0x96);
                  thunk_FUN_0040d040();
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                FUN_004143f0(0);
                cVar2 = FUN_004561b0();
                if ((cVar2 != '\0') && (iVar17 = FUN_00414410(), iVar17 == 2)) {
                  FUN_004143f0(1);
                  pcVar3 = (char *)FUN_0040d0c0();
                  local_204 = (code *)atoi(pcVar3);
                  FUN_0040c340(&DAT_00b1a4ec);
                  local_8 = CONCAT31(local_8._1_3_,0xa2);
                  iVar17 = FUN_0040c2e0();
                  local_23c = iVar17 - 1;
                  piVar8 = (int *)FUN_0041cb60();
                  for (iVar17 = *piVar8; 0 < iVar17; iVar17 = iVar17 + -1) {
                    uVar5 = 10;
                    FUN_0060c530(iVar17);
                    uVar5 = FUN_00694170(uVar5);
                    local_8._0_1_ = 0xa3;
                    FUN_00651af0(uVar5);
                    local_8 = CONCAT31(local_8._1_3_,0xa2);
                    thunk_FUN_0040d040();
                  }
                  FUN_0040d0c0();
                  FUN_00a19440();
                  FUN_00a26620();
                  FUN_0040c340("Copied.\n");
                  local_8._0_1_ = 0xa4;
                  FUN_006929e0(local_64 + 6,0xffd3d3d3,0x96);
                  thunk_FUN_0040d040();
                  thunk_FUN_0040d040();
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                FUN_004143f0(0);
                cVar2 = FUN_004561b0();
                if ((cVar2 != '\0') && (iVar17 = FUN_00414410(), iVar17 == 2)) {
                  FUN_004143f0(1);
                  uVar5 = FUN_0040d0c0();
                  FUN_0086e6c0(uVar5);
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                FUN_004143f0(0);
                cVar2 = FUN_004561b0();
                if (cVar2 == '\0') {
                  FUN_004143f0(0);
                  cVar2 = FUN_004561b0();
                  if (cVar2 != '\0') goto LAB_006918d8;
                }
                else {
LAB_006918d8:
                  uVar6 = FUN_00414410();
                  if (1 < uVar6) {
                    uVar5 = FUN_004143f0(1);
                    FUN_0040cf50(uVar5);
                    local_8 = CONCAT31(local_8._1_3_,0xa5);
                    uVar6 = FUN_00414410();
                    if (2 < uVar6) {
                      uVar19 = 2;
                      uVar6 = FUN_00414410();
                      if (2 < uVar6) {
                        do {
                          uVar5 = FUN_004143f0(uVar19);
                          FUN_00421620(&DAT_00b656ec);
                          local_8._0_1_ = 0xa6;
                          uVar5 = FUN_00651d50(uVar5);
                          FUN_004215a0(uVar5);
                          thunk_FUN_0040d040();
                          local_8 = CONCAT31(local_8._1_3_,0xa5);
                          thunk_FUN_0040d040();
                          uVar19 = uVar19 + 1;
                          uVar6 = FUN_00414410();
                        } while (uVar19 < uVar6);
                      }
                    }
                    FUN_00865660(local_7c,local_ac);
                    local_8._0_1_ = 0xa7;
                    cVar2 = FUN_0040c2d0();
                    if (cVar2 == '\0') {
                      FUN_00692ed0(local_7c);
                    }
                    thunk_FUN_0040d040();
                    thunk_FUN_0040d040();
                    uVar6 = DAT_00c7166c;
                    goto LAB_0069249e;
                  }
                }
                FUN_004143f0(0);
                cVar2 = FUN_004561b0();
                if ((cVar2 != '\0') && (uVar6 = FUN_00414410(), 1 < uVar6)) {
                  uVar5 = FUN_004143f0(1);
                  FUN_0040cf50(uVar5);
                  local_8 = CONCAT31(local_8._1_3_,0xa8);
                  uVar6 = FUN_00414410();
                  if (2 < uVar6) {
                    uVar19 = 2;
                    uVar6 = FUN_00414410();
                    if (2 < uVar6) {
                      do {
                        uVar5 = FUN_004143f0(uVar19);
                        FUN_00421620(&DAT_00b656ec);
                        local_8._0_1_ = 0xa9;
                        uVar5 = FUN_00651d50(uVar5);
                        FUN_004215a0(uVar5);
                        thunk_FUN_0040d040();
                        local_8 = CONCAT31(local_8._1_3_,0xa8);
                        thunk_FUN_0040d040();
                        uVar19 = uVar19 + 1;
                        uVar6 = FUN_00414410();
                      } while (uVar19 < uVar6);
                    }
                  }
                  puVar15 = (undefined4 *)FUN_00684e50((int)&local_218 + 4);
                  uVar5 = *puVar15;
                  puVar15 = (undefined4 *)
                            std::basic_string<char,std::char_traits<char>,std::allocator<char>_>::
                            end(local_7c);
                  uVar22 = *puVar15;
                  puVar15 = (undefined4 *)FUN_00684e50(local_234);
                  FUN_00693eb0(*puVar15,uVar22,uVar5);
                  FUN_0040d210();
                  cVar2 = FUN_008f70f0(local_7c);
                  if (cVar2 == '\0') {
                    FUN_0040c340("Failed to run mod!\n");
                    local_8._0_1_ = 0xab;
                  }
                  else {
                    FUN_0040c340("Success!\n");
                    local_8._0_1_ = 0xaa;
                  }
                  FUN_006929e0(local_64 + 6,0xffd3d3d3,0x96);
                  thunk_FUN_0040d040();
                  thunk_FUN_0040d040();
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                FUN_004143f0(0);
                cVar2 = FUN_004561b0();
                if (cVar2 != '\0') {
                  uVar5 = FUN_00685cc0(4);
                  uVar5 = lua_gc(uVar5);
                  uVar22 = FUN_00685cc0(3,0);
                  uVar22 = lua_gc(uVar22);
                  FUN_00693090(param_1,"Lua mem usage: %d KB and %d bytes\n",uVar22,uVar5);
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                FUN_004143f0(0);
                cVar2 = FUN_004561b0();
                if (cVar2 != '\0') {
                  FUN_0040d210();
                  FUN_008f73f0();
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                FUN_004143f0(0);
                cVar2 = FUN_004561b0();
                if (cVar2 != '\0') {
                  FUN_005cba40();
                  local_8._0_1_ = 0xac;
                  iVar17 = 10000;
                  do {
                    FUN_00685ef0();
                    uVar5 = FUN_006eef60();
                    BossPool__bosspools_xml_consumer(uVar5);
                    FUN_00685ef0();
                    FUN_00424530();
                    uVar5 = FUN_004073c0();
                    FUN_00424530();
                    uVar22 = FUN_0040c3a0();
                    local_1fc = (code *)Level__select_boss_id(uVar22,uVar5,0);
                    FUN_00557b00(&local_21c,&local_1fc);
                    uVar5 = FUN_004561a0((int)&local_218 + 4);
                    cVar2 = FUN_00557bb0(uVar5);
                    if (cVar2 == '\0') {
                      iVar4 = FUN_005cba30();
                      *(int *)(iVar4 + 4) = *(int *)(iVar4 + 4) + 1;
                    }
                    else {
                      local_204 = (code *)0x1;
                      uVar5 = FUN_005cbfa0(&local_204);
                      FUN_005cbfc0(local_238,uVar5);
                    }
                    iVar17 = iVar17 + -1;
                  } while (iVar17 != 0);
                  FUN_0042c770(&local_208);
                  uVar5 = FUN_004561a0(&local_204);
                  cVar2 = FUN_0042c710(uVar5);
                  while (cVar2 != '\0') {
                    piVar8 = (int *)FUN_005cba30();
                    if (*piVar8 < 0) {
                      if (DAT_00c71678 != 0) {
                        uVar22 = FUN_00685ed0();
                        iVar17 = FUN_005cba30();
                        uVar5 = *(undefined4 *)(iVar17 + 4);
                        piVar8 = (int *)FUN_005cba30();
                        iVar17 = -*piVar8;
                        pcVar3 = "%d: %d\n";
                        goto LAB_00691de8;
                      }
                    }
                    else if (DAT_00c71678 != 0) {
                      uVar22 = FUN_00685ed0();
                      iVar17 = FUN_005cba30();
                      uVar5 = *(undefined4 *)(iVar17 + 4);
                      FUN_00417910();
                      puVar15 = (undefined4 *)FUN_005cba30();
                      FUN_0069d200(*puVar15);
                      iVar17 = FUN_0040d0c0();
                      pcVar3 = "%s: %d\n";
LAB_00691de8:
                      FUN_00693090(uVar22,pcVar3,iVar17,uVar5);
                    }
                    FUN_00693270();
                    uVar5 = FUN_004561a0(&local_204);
                    cVar2 = FUN_0042c710(uVar5);
                  }
                  FUN_00436fb0();
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                FUN_004143f0(0);
                cVar2 = FUN_004561b0();
                if (cVar2 == '\0') {
                  FUN_004143f0(0);
                  cVar2 = FUN_004561b0();
                  if (cVar2 != '\0') {
                    FUN_00407480();
                    FUN_007f2070();
                    uVar6 = DAT_00c7166c;
                    goto LAB_0069249e;
                  }
                  FUN_004143f0(0);
                  cVar2 = FUN_004561b0();
                  if (cVar2 != '\0') {
                    FUN_0042ca00();
                    FUN_0040d210();
                    FUN_0040c340("wisps.xml");
                    local_8._0_1_ = 0xaf;
                    FUN_008f5ad0(local_16c,local_64 + 6);
                    local_8._0_1_ = 0xb0;
                    uVar5 = FUN_0040d0c0();
                    FUN_0072a1b0(uVar5,0);
                    thunk_FUN_0040d040();
                    local_8._0_1_ = 0;
                    thunk_FUN_0040d040();
                    FUN_0042ca00();
                    FUN_0040d210();
                    FUN_0040c340("locusts.xml");
                    local_8._0_1_ = 0xb1;
                    FUN_008f5ad0(local_19c,local_2c);
                    local_8._0_1_ = 0xb2;
                    uVar5 = FUN_0040d0c0();
                    FUN_0072ba80(uVar5,0);
                    thunk_FUN_0040d040();
                    local_8._0_1_ = 0;
                    thunk_FUN_0040d040();
                    FUN_00407480();
                    local_21c = FUN_00428a50();
                    pcVar18 = (code *)0x0;
                    local_1fc = (code *)0x0;
                    iVar17 = FUN_004176f0();
                    uVar6 = DAT_00c7166c;
                    if (iVar17 != 0) {
                      do {
                        puVar15 = (undefined4 *)FUN_00417620(pcVar18);
                        piVar8 = (int *)*puVar15;
                        local_20c = piVar8;
                        cVar2 = FUN_00417220(3,0xce,0xffffffff);
                        if (cVar2 == '\0') {
                          cVar2 = FUN_00417220(3,0xe7,0xffffffff);
                          if (cVar2 != '\0') {
                            local_204 = *(code **)(*piVar8 + 4);
                            uVar5 = FUN_00505b70();
                            uVar22 = FUN_00417280();
                            uVar21 = FUN_00417270();
                            uVar23 = FUN_00417260();
                            (*local_204)(uVar23,uVar21,uVar22,uVar5);
                          }
                        }
                        else {
                          local_204 = *(code **)(*piVar8 + 4);
                          uVar5 = FUN_00505b70();
                          uVar22 = FUN_00417280();
                          uVar21 = FUN_00417270();
                          uVar23 = FUN_00417260();
                          (*local_204)(uVar23,uVar21,uVar22,uVar5);
                        }
                        pcVar18 = local_1fc + 1;
                        local_1fc = pcVar18;
                        pcVar14 = (code *)FUN_004176f0();
                        uVar6 = DAT_00c7166c;
                      } while (pcVar18 < pcVar14);
                    }
                    goto LAB_0069249e;
                  }
                  FUN_004143f0(0);
                  cVar2 = FUN_004561b0();
                  if (cVar2 != '\0') {
                    FUN_00706020(0);
                    uVar21 = 0;
                    uVar22 = 0;
                    uVar5 = FUN_0042a340();
                    FUN_009e9320(uVar5);
                    FUN_00958cb0(in_stack_fffffd40,in_stack_fffffd44,in_stack_fffffd48,
                                 in_stack_fffffd4c,in_stack_fffffd50,in_stack_fffffd54,
                                 in_stack_fffffd58,in_stack_fffffd5c,in_stack_fffffd60,
                                 in_stack_fffffd64,in_stack_fffffd68,in_stack_fffffd6c,
                                 in_stack_fffffd70,in_stack_fffffd74,in_stack_fffffd78,
                                 in_stack_fffffd7c,in_stack_fffffd80,in_stack_fffffd84,
                                 in_stack_fffffd88,in_stack_fffffd8c,in_stack_fffffd90,
                                 in_stack_fffffd94,in_stack_fffffd98,uVar22,uVar21);
                    uVar5 = FUN_0042a340();
                    FUN_009e9430(uVar5);
                    iVar17 = DAT_00c7169c;
                    *(undefined1 *)(DAT_00c7169c + 0x4b284) = 1;
                    *(undefined1 *)(iVar17 + 0x4b131) = 1;
                    FUN_00685ee0();
                    uVar6 = DAT_00c7166c;
                    goto LAB_0069249e;
                  }
                  FUN_004143f0(0);
                  cVar2 = FUN_004561b0();
                  if (cVar2 != '\0') {
                    FUN_00686110();
                    uVar6 = DAT_00c7166c;
                    goto LAB_0069249e;
                  }
                  FUN_004143f0(0);
                  cVar2 = FUN_004561b0();
                  uVar6 = DAT_00c7166c;
                  if (cVar2 == '\0') goto LAB_0069249e;
                  iVar17 = FUN_00414410();
                  if (iVar17 == 2) {
                    FUN_004143f0(1);
                    FUN_0040d0c0();
                    pcVar18 = (code *)FUN_009036b0();
                    if (pcVar18 == (code *)0x0) {
                      FUN_0040c340("Successfully fixed history log.\n");
                      local_8._0_1_ = 0xb3;
                      goto LAB_00691611;
                    }
                    pcVar3 = "Fixed to fix history log: %s\n";
                  }
                  else {
                    iVar17 = FUN_00414410();
                    pcVar18 = (code *)(iVar17 + -1);
                    pcVar3 = "Invalid number of parameters: expected 1, found %d.\n";
                  }
LAB_00692495:
                  FUN_00693090(param_1,pcVar3,pcVar18);
                  uVar6 = DAT_00c7166c;
                  goto LAB_0069249e;
                }
                local_200 = 0xffffffff;
                local_1fc = (code *)0x0;
                uVar6 = FUN_00414410();
                if (1 < uVar6) {
                  FUN_004143f0(1);
                  pcVar3 = (char *)FUN_0040d0c0();
                  local_1fc = (code *)atoi(pcVar3);
                }
                uVar6 = FUN_00414410();
                if (uVar6 < 3) {
LAB_00691ed6:
                  local_218 = 0;
                  uVar6 = 0;
                  iVar17 = FUN_004178d0();
                  uVar19 = (uint)local_218;
                  uVar9 = local_218._4_4_;
                  if (iVar17 != 0) {
                    do {
                      PlayerManager__get_player_417870(uVar6);
                      uVar12 = FUN_00423950();
                      uVar16 = 1 << (uVar12 & 0x1f);
                      uVar13 = 0;
                      if (0x1f < uVar12) {
                        uVar13 = uVar16;
                      }
                      uVar16 = uVar16 ^ uVar13;
                      if (0x3f < uVar12) {
                        uVar13 = uVar16;
                      }
                      uVar19 = uVar19 | uVar16;
                      uVar9 = uVar9 | uVar13;
                      uVar6 = uVar6 + 1;
                      uVar16 = FUN_004178d0();
                    } while (uVar6 < uVar16);
                  }
                  uVar16 = 0;
                  iVar17 = FUN_00a20020();
                  uVar6 = local_200;
                  if (iVar17 != 0) {
                    do {
                      FUN_00a20240(&local_218,uVar16);
                      local_8._0_1_ = 0xad;
                      iVar17 = FUN_0040c3a0();
                      if (iVar17 != 0) {
                        uVar6 = 1 << (uVar16 & 0x1f);
                        uVar13 = 0;
                        if (0x1f < uVar16) {
                          uVar13 = uVar6;
                        }
                        uVar6 = uVar6 ^ uVar13;
                        if (0x3f < uVar16) {
                          uVar13 = uVar6;
                        }
                        if ((uVar6 & uVar19) == 0 && (uVar13 & uVar9) == 0) {
                          piVar8 = (int *)FUN_0040c3a0();
                          _MaxCount = 8;
                          pcVar10 = "Wireless";
                          pcVar3 = (char *)(**(code **)(*piVar8 + 0xc))();
                          iVar17 = strncmp(pcVar3,pcVar10,_MaxCount);
                          if (iVar17 != 0) {
                            FUN_0040c3a0();
                            uVar6 = FUN_004176f0();
                            local_8._0_1_ = 0;
                            FUN_004242b0();
                            break;
                          }
                        }
                      }
                      local_8._0_1_ = 0;
                      FUN_004242b0();
                      uVar16 = uVar16 + 1;
                      uVar13 = FUN_00a20020();
                      uVar6 = local_200;
                    } while (uVar16 < uVar13);
                  }
                  if ((int)uVar6 < 0) {
                    uVar6 = 0;
                  }
                }
                else {
                  FUN_004143f0(2);
                  pcVar3 = (char *)FUN_0040d0c0();
                  uVar6 = atoi(pcVar3);
                  local_200 = uVar6;
                  if ((int)uVar6 < 0) goto LAB_00691ed6;
                }
                if (DAT_00c71678 != 0) {
                  uVar5 = FUN_00685ed0();
                  FUN_00a20390(local_b4,uVar6);
                  local_8 = CONCAT31(local_8._1_3_,0xae);
                  local_21c = 1;
                  piVar8 = (int *)FUN_0040c3a0();
                  uVar22 = (**(code **)(*piVar8 + 0xc))();
                  FUN_00693090(uVar5,"controller id %d %s\n",uVar6,uVar22);
                }
                local_8._0_1_ = 0;
                local_8._1_3_ = 0;
                if ((local_21c & 1) != 0) {
                  FUN_004242b0();
                }
                FUN_00417860();
                FUN_009b9cd0(local_1fc);
                FUN_007a6450(uVar6,0);
                PlayerManager__get_player_417870(0);
                FUN_00417290(local_b4);
                uVar5 = FUN_0067f070(&local_218);
                local_204 = (code *)0x41200000;
                uVar5 = FUN_004171d0(uVar5);
                uVar5 = FUN_00a10420(local_238,uVar5);
                FUN_004288f0(uVar5);
                FUN_004178e0();
                FUN_009a8620();
                FUN_007bc740();
                uVar6 = DAT_00c7166c;
                goto LAB_0069249e;
              }
              FUN_00407480();
              FUN_00815ae0();
              FUN_0040c340("Shop is fully restocked.\n");
              local_8._0_1_ = 0x3b;
            }
            else {
              FUN_004143f0(1);
              pcVar3 = (char *)FUN_0040d0c0();
              uVar6 = atoi(pcVar3);
              if (uVar6 < 0x1b) {
                FUN_00958e60(uVar6,0,1);
                uVar6 = DAT_00c7166c;
                goto LAB_0069249e;
              }
              FUN_0040c340("Invalid cutscene ID.\n");
              local_8._0_1_ = 0x3a;
            }
            goto LAB_0068d95d;
          }
          uVar5 = 0x2e;
          FUN_004143f0(1);
          FUN_0067f580(uVar5);
          local_8._0_1_ = 0x39;
          iVar4 = 1;
          local_200 = 0;
          iVar17 = FUN_00414410();
          pcVar18 = atoi_exref;
          if (iVar17 != 0) {
            FUN_004143f0(0);
            iVar17 = FUN_0040c2e0();
            if (iVar17 != 0) {
              FUN_004143f0(0);
              pcVar3 = (char *)FUN_0040d0c0();
              local_200 = atoi(pcVar3);
              pcVar18 = atoi_exref;
              if (((int)local_200 < 0) || (0x1e < (int)local_200)) {
                local_200 = 0;
              }
            }
          }
          uVar6 = FUN_00414410();
          if (uVar6 < 2) {
LAB_0068fc25:
            do {
              FUN_0042a330();
              uVar5 = FUN_006eef60();
              uVar5 = FUN_00733610(local_200,uVar5,0,0,0);
              FUN_0075f0e0(uVar5,0xffffffff,1,0,0,0);
              iVar4 = iVar4 + -1;
            } while (iVar4 != 0);
          }
          else {
            FUN_004143f0(1);
            iVar17 = FUN_0040c2e0();
            if (iVar17 == 0) goto LAB_0068fc25;
            FUN_004143f0(1);
            uVar5 = FUN_0040d0c0();
            iVar4 = (*pcVar18)(uVar5);
            if (0 < iVar4) goto LAB_0068fc25;
          }
          thunk_FUN_004147f0();
          uVar6 = DAT_00c7166c;
          goto LAB_0069249e;
        }
        FUN_004143f0(1);
        pcVar3 = (char *)FUN_0040d0c0();
        local_20c = (int *)atoi(pcVar3);
        uVar19 = 1;
        uVar6 = DAT_00c7166c;
        if ((int)local_20c < 1) goto LAB_0069249e;
        local_204 = (code *)0x2710;
        puVar15 = (undefined4 *)FUN_0041cb60();
        local_20c = (int *)*puVar15;
        uVar6 = FUN_0040c2e0();
        if (1 < uVar6) {
          do {
            FUN_0060c560(&local_70);
            FUN_00693560(local_b8,uVar19);
            FUN_0060c420();
            iVar17 = FUN_00557b70("repeat",0);
            param_4 = local_208;
            if (iVar17 == -1) break;
            uVar19 = uVar19 + 1;
            uVar6 = FUN_0040c2e0();
            param_4 = local_208;
          } while (uVar19 < uVar6);
        }
        uVar6 = FUN_0040c2e0();
        if (uVar19 < uVar6) {
          FUN_0060c560(&local_70);
          FUN_00693560(local_b8,uVar19);
          uVar5 = FUN_0060c420();
          FUN_0040cf50(uVar5);
          piVar8 = local_20c;
          local_8._0_1_ = 0x2e;
          uVar5 = FUN_0040d0c0();
          FUN_00693090(param_1,">%s (x%d)\n",uVar5,piVar8);
          iVar17 = 0;
          if (0 < (int)local_20c) {
            do {
              Game__boss_pool_state_loader(local_ac,0,param_4);
              iVar17 = iVar17 + 1;
            } while (iVar17 < (int)local_20c);
          }
          thunk_FUN_0040d040();
          uVar6 = DAT_00c7166c;
          goto LAB_0069249e;
        }
        FUN_0040c340("Nothing to repeat.\n");
        local_8._0_1_ = 0x2d;
      }
      else {
        uVar6 = 1;
        local_1e5 = '\x01';
        local_200 = 1;
        FUN_0042ca00();
        FUN_00424530();
        iVar17 = FUN_00417840();
        if (1 < iVar17) {
          do {
            cVar2 = FUN_007706e0(uVar6,0);
            if (cVar2 != '\0') {
              if (local_1e5 == '\0') {
                FUN_0040c340(&DAT_00b66304);
                local_8._0_1_ = 0x2a;
                FUN_006929e0(local_94,0xffd3d3d3,0x96);
                local_8._0_1_ = 0;
                thunk_FUN_0040d040();
              }
              uVar5 = FUN_00770ca0(uVar6,0);
              FUN_0042ca00();
              FUN_0072fd10(local_200);
              FUN_0072ff10(local_64 + 6,0);
              local_8._0_1_ = 0x2b;
              uVar22 = FUN_0040d0c0();
              FUN_00693090(param_1,"%s:%d",uVar22,uVar5);
              local_8._0_1_ = 0;
              thunk_FUN_0040d040();
              local_1e5 = '\0';
              uVar6 = local_200;
            }
            uVar6 = uVar6 + 1;
            local_200 = uVar6;
            FUN_0042ca00();
            FUN_00424530();
            iVar17 = FUN_00417840();
          } while ((int)uVar6 < iVar17);
        }
        FUN_0040c340(&DAT_00b66310);
        local_8._0_1_ = 0x2c;
      }
    }
    else {
      uVar6 = FUN_00414410();
      if (2 < uVar6) {
        FUN_004143f0(1);
        pcVar3 = (char *)FUN_0040d0c0();
        local_21c = atoi(pcVar3);
        FUN_004143f0(2);
        pcVar3 = (char *)FUN_0040d0c0();
        local_1fc = (code *)atoi(pcVar3);
        uVar6 = FUN_00414410();
        if (uVar6 < 4) {
          uVar6 = 0xffffffff;
        }
        else {
          FUN_004143f0(3);
          pcVar3 = (char *)FUN_0040d0c0();
          uVar6 = atoi(pcVar3);
        }
        if (((local_21c < 0xd) && (local_1fc < &DAT_0000000d)) && (uVar6 < 3)) {
          FUN_00424530();
          local_204 = (code *)((int)local_1fc * 0xd + local_21c);
          iVar17 = FUN_00740da0(local_204,uVar6);
          if (*(int *)(iVar17 + 0x10) != 0) {
            FUN_006fd7c0(local_204,0xffffffff,1,param_4,uVar6);
            FUN_0040c340("Changed room.\n");
            local_8._0_1_ = 0xf;
            goto LAB_0068d95d;
          }
        }
        FUN_0040c340("Error changing room.\n");
        local_8._0_1_ = 0x10;
        goto LAB_0068d95d;
      }
      iVar17 = FUN_00414410();
      uVar6 = DAT_00c7166c;
      if (iVar17 != 2) goto LAB_0069249e;
      FUN_004143f0(1);
      pcVar3 = (char *)FUN_004170e0(1);
      uVar6 = DAT_00c7166c;
      if (*pcVar3 != '.') goto LAB_0069249e;
      FUN_004143f0(1);
      pcVar3 = (char *)FUN_004170e0(0);
      local_1e5 = *pcVar3;
      if ((local_1e5 == 's') || (local_1e5 == 'x')) {
        FUN_004143f0(1);
        FUN_00651a90(local_ac,2,0xffffffff);
        local_8._0_1_ = 0x11;
        FUN_0067f580(0x2e);
        local_8._0_1_ = 0x12;
        FUN_004143f0(0);
        local_204 = (code *)FUN_0082d100();
        local_8._0_1_ = 0x11;
        thunk_FUN_004147f0();
        iVar17 = 0;
        FUN_0067f580(0x2e);
        local_8._0_1_ = 0x13;
        uVar6 = FUN_00414410();
        if (1 < uVar6) {
          FUN_004143f0(1);
          iVar4 = FUN_0040c2e0();
          if (iVar4 != 0) {
            FUN_004143f0(1);
            pcVar3 = (char *)FUN_0040d0c0();
            iVar17 = atoi(pcVar3);
          }
        }
        FUN_00421790();
        if (local_1e5 == 'x') {
          FUN_00424530();
          uVar5 = FUN_00738470(0);
        }
        else {
          uVar5 = 0;
        }
        iVar17 = RoomConfig__get_room(uVar5,local_204,iVar17,0xffffffff);
        thunk_FUN_004147f0();
        local_8._0_1_ = 0;
        thunk_FUN_0040d040();
LAB_0068dccb:
        if (iVar17 != 0) {
          FUN_00424530();
          FUN_0073fa20(iVar17);
          FUN_0040c340("Changed room.\n");
          local_8._0_1_ = 0x14;
          goto LAB_0068d95d;
        }
      }
      else if (local_1e5 == 'd') {
        FUN_004143f0(1);
        FUN_00651a90(local_64 + 6,2,0xffffffff);
        pcVar3 = (char *)FUN_0040d0c0();
        iVar17 = atoi(pcVar3);
        thunk_FUN_0040d040();
        FUN_00421790();
        FUN_00424530();
        uVar5 = FUN_00738470(0);
        iVar17 = RoomConfig__get_room(uVar5,1,iVar17,0xffffffff);
        goto LAB_0068dccb;
      }
      FUN_0040c340("Error changing room.\n");
      local_8._0_1_ = 0x15;
    }
LAB_0068d95d:
    FUN_006929e0(local_94,0xffd3d3d3,0x96);
    thunk_FUN_0040d040();
    uVar6 = DAT_00c7166c;
    goto LAB_0069249e;
  }
  local_8._0_1_ = 1;
  FUN_00424510();
  local_21c = 4;
  FUN_0067f420(&local_70);
  local_22c = 0;
  local_1fc = (code *)0x0;
  local_230 = 0;
  local_1f5 = '\0';
  local_1e5 = '\0';
  local_200 = 0xffffffff;
  iVar17 = local_6c - local_70 >> 0x1f;
  if ((local_6c - local_70) / 0x18 + iVar17 != iVar17) {
    pcVar3 = (char *)FUN_0040d0c0();
    local_22c = atoi(pcVar3);
  }
  if (1 < (uint)((local_6c - local_70) / 0x18)) {
    pcVar3 = (char *)FUN_0040d0c0();
    local_1fc = (code *)atoi(pcVar3);
  }
  if (2 < (uint)((local_6c - local_70) / 0x18)) {
    pcVar3 = (char *)FUN_0040d0c0();
    local_230 = atoi(pcVar3);
  }
  if (3 < (uint)((local_6c - local_70) / 0x18)) {
    iVar17 = 0;
    while( true ) {
      while( true ) {
        puVar15 = (undefined4 *)(local_70 + 0x48);
        if (0xf < *(uint *)(local_70 + 0x5c)) {
          puVar15 = (undefined4 *)*puVar15;
        }
        iVar4 = tolower((int)*(char *)((int)puVar15 + iVar17));
        if ((char)iVar4 != 'f') break;
        iVar17 = iVar17 + 1;
        local_1f5 = '\x01';
      }
      if ((char)iVar4 != 'p') break;
      iVar17 = iVar17 + 1;
      local_1e5 = '\x01';
    }
    puVar15 = (undefined4 *)(local_70 + 0x48);
    if (0xf < *(uint *)(local_70 + 0x5c)) {
      puVar15 = (undefined4 *)*puVar15;
    }
    if (*(char *)((int)puVar15 + iVar17) == '\0') {
      local_200 = 0xffffffff;
    }
    else {
      local_200 = iVar17;
      iVar4 = FUN_0040d0c0();
      local_200 = atoi((char *)(iVar4 + iVar17));
    }
  }
  uVar5 = FUN_00812d00(&local_218);
  FUN_00813520(local_b4,uVar5,0,0,0,0);
  iVar17 = *(int *)(DAT_00c71678 + 0x18300);
  uVar6 = FUN_00812c90(local_b4);
  if (uVar6 < 0x1c0) {
    *(undefined4 *)(iVar17 + 0x76c + uVar6 * 4) = 900;
  }
  iVar17 = 0;
  local_208 = 0;
  if (local_22c == 1) {
    iVar17 = FUN_009b98e0(local_230 - 1);
    local_208 = iVar17;
    __RTDynamicCast(iVar17,0,&IsaacRepentancePlus::Entity::RTTI_Type_Descriptor,
                    &IsaacRepentancePlus::Entity_Player::RTTI_Type_Descriptor,0);
    FUN_007cb090();
    FUN_009a8620();
  }
  else if (local_22c != 0) {
    uVar5 = FUN_006eef60();
    iVar17 = FUN_00428b20(local_22c,local_1fc,local_b4,&DAT_00c7b640,0,local_230,uVar5);
    local_208 = iVar17;
  }
  local_1fc = (code *)__RTDynamicCast(iVar17,0,&IsaacRepentancePlus::Entity::RTTI_Type_Descriptor,
                                      &IsaacRepentancePlus::Entity_NPC::RTTI_Type_Descriptor,0);
  if ((local_1fc != (code *)0x0) && (-1 < (int)local_200)) {
    FUN_006c0f30(*(int *)(local_1fc + 0x28),*(int *)(local_1fc + 0x2c),*(int *)(local_1fc + 0x30),
                 local_200);
  }
  if (local_1e5 != '\0') {
    if (param_4 == 0) {
      iVar4 = 0;
    }
    else {
      iVar4 = *(int *)(param_4 + 0x1618);
    }
    *(int *)(local_1fc + 0xf1c) = iVar4;
  }
  if ((iVar17 == 0) || (*(int *)(iVar17 + 0x28) == 0)) {
    pcVar18 = (code *)(DAT_00c7169c + 0x2a670);
    local_204 = pcVar18;
    FUN_006936e0(**(undefined4 **)pcVar18,pcVar18);
    FUN_006936e0(*(int *)pcVar18,pcVar18);
    if (local_200 != local_22c) {
      do {
        if ((iVar17 != 0) && (*(int *)(iVar17 + 0x28) != 0)) goto LAB_0068d54c;
        local_1fc = (code *)(local_200 + 0x18);
        if ((*(int *)local_1fc != 5) ||
           ((*(int *)(local_200 + 0x1c) != 300 || (*(int *)(local_200 + 0x20) == 0)))) {
          FUN_0040cca0(local_204);
          FUN_0040cfe0();
          local_8._0_1_ = 3;
          if (1 < (uint)((local_1f0 - local_1f4) / 0x18)) {
            if (local_184 !=
                (basic_string<char,std::char_traits<char>,std::allocator<char>_> *)
                (local_1f4 + 0x18)) {
              local_230 = local_230 & 0xffffff00;
              FUN_0040c720((basic_string<char,std::char_traits<char>,std::allocator<char>_> *)
                           (local_1f4 + 0x18),local_230);
            }
            if (2 < (uint)((local_1f0 - local_1f4) / 0x18)) {
              uVar6 = 2;
              iVar17 = 0x30;
              do {
                iVar4 = local_1f4 + iVar17;
                FUN_00421620(&DAT_00b656ec);
                local_8 = CONCAT31(local_8._1_3_,4);
                pbVar7 = (basic_string<char,std::char_traits<char>,std::allocator<char>_> *)
                         FUN_00651d50(iVar4);
                if (local_184 != pbVar7) {
                  local_23c = local_23c & 0xffffff00;
                  FUN_004215e0(pbVar7,local_23c);
                }
                FUN_0040d040();
                local_8._0_1_ = 3;
                FUN_0040d040();
                uVar6 = uVar6 + 1;
                iVar17 = iVar17 + 0x18;
              } while (uVar6 < (uint)((local_1f0 - local_1f4) / 0x18));
            }
            puVar15 = (undefined4 *)FUN_00684e50(local_24c);
            uVar5 = *puVar15;
            puVar15 = (undefined4 *)
                      std::basic_string<char,std::char_traits<char>,std::allocator<char>_>::end
                                (local_184);
            uVar22 = *puVar15;
            puVar15 = (undefined4 *)FUN_00684e50(local_244);
            FUN_00693eb0(*puVar15,uVar22,uVar5);
          }
          FUN_00694d20(local_ac,0);
          local_8._0_1_ = 5;
          puVar15 = (undefined4 *)FUN_00684e50(local_220);
          uVar5 = *puVar15;
          puVar15 = (undefined4 *)
                    std::basic_string<char,std::char_traits<char>,std::allocator<char>_>::end
                              (local_ac);
          uVar22 = *puVar15;
          puVar15 = (undefined4 *)FUN_00684e50(local_224);
          FUN_00693eb0(*puVar15,uVar22,uVar5);
          iVar4 = FUN_00693650(local_184,0);
          iVar17 = local_208;
          if (iVar4 != -1) {
            iVar17 = *(int *)local_1fc;
            iVar4 = *(int *)(local_1fc + 4);
            iVar1 = *(int *)(local_1fc + 8);
            uVar5 = FUN_006eef60();
            iVar17 = FUN_00428b20(iVar17,iVar4,local_b4,&DAT_00c7b640,0,iVar1,uVar5);
            local_208 = iVar17;
            FUN_0040c340("Spawned entity.\n");
            local_8._0_1_ = 6;
            FUN_006929e0(local_94,0xffd3d3d3,0x96);
            FUN_0040d040();
          }
          FUN_0040d040();
          local_8._0_1_ = 1;
          FUN_0040d040();
          pcVar18 = local_204;
        }
        std::
        _Tree_unchecked_const_iterator<std::_Tree_val<std::_Tree_simple_types<unsigned_int>_>,std::_Iterator_base0>
        ::operator++((_Tree_unchecked_const_iterator<std::_Tree_val<std::_Tree_simple_types<unsigned_int>_>,std::_Iterator_base0>
                      *)&local_200);
        FUN_006936e0(*(int *)pcVar18,pcVar18);
      } while (local_200 != local_22c);
    }
    if ((iVar17 != 0) && (*(int *)(iVar17 + 0x28) != 0)) goto LAB_0068d54c;
    FUN_0040c340("Error spawning entity.\n");
    local_8._0_1_ = 7;
    FUN_006929e0(local_94,0xffd3d3d3,0x96);
    local_8._0_1_ = 1;
    FUN_0040d040();
    if (iVar17 != 0) goto LAB_0068d54c;
  }
  else {
    FUN_0040c340("Spawned entity.\n");
    local_8._0_1_ = 2;
    FUN_006929e0(local_ac,0xffd3d3d3,0x96);
    local_8._0_1_ = 1;
    FUN_0040d040();
LAB_0068d54c:
    if (local_1f5 != '\0') {
      FUN_00431310(0);
      FUN_006ad870(local_64 + 2,0xffffffff,0,0);
    }
  }
  FUN_004147f0();
  uVar6 = DAT_00c7166c;
LAB_0069249e:
  DAT_00c7166c = uVar6;
  thunk_FUN_004147f0();
  ExceptionList = local_10;
  return;
}
