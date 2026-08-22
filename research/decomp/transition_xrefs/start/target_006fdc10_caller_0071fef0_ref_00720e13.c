/* Static decompilation only; PE entry point was not executed. */
/* Target: 006fdc10 */
/* Reference: 00720e13 */
/* Caller: FUN_0071fef0 @ 0071fef0 */


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0071fef0(int param_1)

{
  char *pcVar1;
  byte bVar2;
  undefined3 uVar3;
  char cVar4;
  uint uVar5;
  int iVar6;
  uint uVar7;
  uint uVar8;
  uint *puVar9;
  int *piVar10;
  byte *pbVar11;
  byte *pbVar12;
  char ******ppppppcVar13;
  int *piVar14;
  int iVar15;
  uint uVar16;
  char *pcVar17;
  undefined3 extraout_var;
  int extraout_EDX;
  int extraout_EDX_00;
  float fVar18;
  undefined4 uVar19;
  bool bVar20;
  float fVar21;
  float fVar22;
  float fVar23;
  double dVar24;
  char local_68 [4];
  int local_64;
  uint local_5c;
  float local_58;
  uint local_54;
  int local_50;
  float local_4c;
  char *local_48;
  float local_44;
  float local_40;
  int *local_3c;
  char local_35;
  int *local_34;
  char local_2d;
  char *****local_2c [4];
  undefined4 local_1c;
  uint local_18;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;

  piVar14 = DAT_00c71678;
  local_8 = 0xffffffff;
  puStack_c = &LAB_00afccc9;
  local_10 = ExceptionList;
  uVar5 = DAT_00bf93b4 ^ (uint)&stack0xfffffffc;
  ExceptionList = &local_10;
  local_54 = 0;
  *(int *)(param_1 + 0x154) = *(int *)(param_1 + 0x154) + 1;
  local_4c = (float)(*(int *)(param_1 + 0x24) % *(int *)(piVar14[0x60c0] + 0xc)) * DAT_00baa904 +
             DAT_00baa904;
  local_48 = (char *)((float)(*(int *)(param_1 + 0x24) / *(int *)(piVar14[0x60c0] + 0xc)) *
                      DAT_00baa904 + DAT_00baaa00);
  local_50 = param_1;
  local_14 = uVar5;
  local_44 = (float)FUN_00703ab0(&local_4c,1,0,0);
  local_34._0_1_ = false;
  local_40 = DAT_00baacb8;
  iVar6 = DAT_00c71678[0x60c0];
  local_58 = DAT_00baa880;
  if ((((*(int *)(iVar6 + 8) == 5) &&
       (piVar14 = *(int **)(*(int *)(iVar6 + 4) + 0x10), *piVar14 == 0)) && (piVar14[4] == 0x58)) &&
     (*(int *)(param_1 + 0x18) != 1)) {
    local_35 = '\x01';
    local_58 = DAT_00baa8e8;
  }
  else {
    local_35 = '\0';
  }
  iVar15 = *(int *)(param_1 + 0x24);
  if (local_44 == 0.0) {
    local_3c = *(int **)(iVar6 + 0xc);
  }
  else {
    local_3c = *(int **)(iVar6 + 0xc);
    fVar21 = ((float)(iVar15 / (int)local_3c) * DAT_00baa904 + DAT_00baaa00) -
             *(float *)((int)local_44 + 0x340);
    fVar23 = ((float)(iVar15 % (int)local_3c) * DAT_00baa904 + DAT_00baa904) -
             *(float *)((int)local_44 + 0x33c);
    fVar21 = fVar21 * fVar21 + fVar23 * fVar23;
    local_34._1_3_ = extraout_var;
    FUN_00435a50(uVar5);
    local_34._0_1_ = fVar21 < DAT_00baa924;
    local_40 = fVar21;
  }
  local_34._1_3_ = 0;
  if (((*(int *)(DAT_00c7169c + 0x4b3d8) != *(int *)(DAT_00c7169c + 0x4b3dc)) &&
      (1 < (uint)(*(int *)(DAT_00c7169c + 0x4b3dc) - *(int *)(DAT_00c7169c + 0x4b3d8) >> 2))) &&
     ((*(int *)(param_1 + 0x10) < 2 && ((*(int *)(iVar6 + 8) == 5 && (local_35 == '\0')))))) {
    local_34._1_3_ = (undefined3)((uint)param_1 >> 8);
    if (((bool)(char)local_34 == false) && (0x95 < *(uint *)(param_1 + 0x154))) {
      local_34._0_1_ = false;
    }
    else {
      local_34._0_1_ = true;
    }
  }
  uVar3 = local_34._1_3_;
  bVar20 = (bool)(char)local_34;
  local_4c = (float)(iVar15 % (int)local_3c) * DAT_00baa904 + DAT_00baa904;
  local_48 = (char *)((float)(iVar15 / (int)local_3c) * DAT_00baa904 + DAT_00baaa00);
  FUN_0041a790(local_68,&local_4c,1);
  uVar5 = 0;
  local_8 = 0;
  if (local_5c != 0) {
    do {
      local_34._1_3_ = uVar3;
      local_34._0_1_ = bVar20;
      if ((bool)(char)local_34 != false) break;
      iVar6 = *(int *)(local_64 + uVar5 * 4);
      if (*(int *)(iVar6 + 0x28) == 3) {
        local_34._0_1_ = false;
        local_34._1_3_ = 0;
        if (*(int *)(iVar6 + 0x2c) == 900) {
          local_34._0_1_ = true;
          local_34._1_3_ = 0;
        }
      }
      uVar5 = uVar5 + 1;
      bVar20 = (bool)(char)local_34;
      uVar3 = local_34._1_3_;
    } while (uVar5 < local_5c);
  }
  if ((((DAT_00c71678[0x9a72] != 2) && (DAT_00c71678[0x9a72] != 3)) &&
      (iVar6 = PlayerManager__FirstCollectibleOwner(0x226,DAT_00c71678 + 0x6eaa,1), iVar6 != 0)) &&
     (*(int *)(DAT_00c71678[0x60c0] + 8) != 3)) {
    iVar6 = *DAT_00c71678;
    uVar5 = DAT_00c71678[0x9954];
    uVar16 = DAT_00c71678[3];
    uVar7 = Level__combined_curse_add_mask();
    uVar8 = Level__combined_curse_remove_mask();
    piVar14 = DAT_00c71678;
    iVar15 = iVar6 + 1;
    if ((~uVar8 & (uVar7 | uVar5 | uVar16) & 2) == 0) {
      iVar15 = iVar6;
    }
    if (iVar15 == 6) {
      if ((*(int *)(*(int *)ThreadLocalStoragePointer + 0xc) < DAT_00c8108c) &&
         (FUN_00aef29d(), DAT_00c8108c == -1)) {
        local_8._0_1_ = 1;
        FUN_006ef590();
        _atexit(FUN_00b15b30);
        local_8 = (uint)local_8._1_3_ << 8;
        FUN_00aef253(&DAT_00c8108c);
      }
      puVar9 = &DAT_00c810d4;
      if ((uint)piVar14[0x60c3] < 3) {
        puVar9 = (uint *)(piVar14 + 0x5be8);
      }
      if ((*puVar9 >> 3 & 1) == 0) {
        local_34._0_1_ = '\x01';
      }
      local_34._1_3_ = 0;
    }
  }
  piVar14 = DAT_00c71678;
  local_48 = *(char **)(DAT_00c71678[0x60c0] + 8);
  if ((local_48 == (char *)0x1b) &&
     ((*(byte *)(*(int *)(DAT_00c71678[0x60c0] + 4) + 0x44) & 1) == 0)) {
    local_34._0_1_ = '\x01';
  }
  local_3c = (int *)*DAT_00c71678;
  if (((0 < (int)local_3c) && ((int)local_3c < 7)) && ((DAT_00c71678[0x9953] & 0x10000U) != 0)) {
    local_34._0_1_ = '\x01';
  }
  if (DAT_00c71678[0x998c] == 0) {
    uVar16 = (*(int *)(DAT_00c7169c + 0x2a668) - *(int *)(DAT_00c7169c + 0x2a664)) / 0xa4 - 1;
    uVar5 = -(uint)(DAT_00c71678[0x9961] != 0) & DAT_00c71678[0x9961];
    if (uVar16 <= uVar5) {
      uVar5 = uVar16;
    }
    piVar10 = (int *)(uVar5 * 0xa4 + *(int *)(DAT_00c7169c + 0x2a664));
  }
  else {
    piVar10 = DAT_00c71678 + 0x9990;
  }
  if (piVar10[0x20] == 2) {
    uVar5 = DAT_00c71678[3];
    uVar16 = DAT_00c71678[0x9954];
    uVar7 = Level__combined_curse_add_mask();
    uVar8 = Level__combined_curse_remove_mask();
    piVar10 = (int *)((int)local_3c + 1);
    if ((~uVar8 & (uVar7 | uVar5 | uVar16) & 2) == 0) {
      piVar10 = local_3c;
    }
    local_3c = piVar10;
    if (*(int *)(piVar14[0x60c0] + 8) == 0x1b) {
      uVar5 = piVar14[3];
      uVar16 = piVar14[0x9954];
      uVar7 = Level__combined_curse_add_mask();
      uVar8 = Level__combined_curse_remove_mask();
      uVar5 = (~uVar8 & (uVar7 | uVar5 | uVar16)) >> 1;
      if ((local_3c == (int *)0x2) || (((uVar5 & 1) != 0 && (local_3c == (int *)0x1)))) {
        bVar20 = true;
      }
      else {
        bVar20 = false;
      }
      if ((local_3c == (int *)&DAT_00000004) || (((uVar5 & 1) != 0 && (local_3c == (int *)0x3)))) {
        local_2d = '\x01';
      }
      else {
        local_2d = '\0';
      }
      if (((!bVar20) ||
          (((piVar14[1] != 4 && (piVar14[1] != 5)) ||
           (iVar6 = PlayerManager__FirstCollectibleOwner(0x272,piVar14 + 0x6eaa,1),
           piVar14 = DAT_00c71678, iVar6 != 0)))) &&
         (((local_2d == '\0' || ((piVar14[1] != 4 && (piVar14[1] != 5)))) ||
          (iVar6 = PlayerManager__FirstCollectibleOwner(0x273,piVar14 + 0x6eaa,1), iVar6 != 0))))
      goto LAB_00720400;
    }
    else {
      if (piVar10 != (int *)&DAT_00000006) {
        uVar5 = piVar14[3];
        uVar16 = piVar14[0x9954];
        uVar7 = Level__combined_curse_add_mask();
        uVar8 = Level__combined_curse_remove_mask();
        if (((~uVar8 & (uVar7 | uVar5 | uVar16) & 2) == 0) || (local_3c != (int *)&DAT_00000005))
        goto LAB_00720400;
      }
      if (((piVar14[1] != 4) && (piVar14[1] != 5)) ||
         (((cVar4 = FUN_0074e9b0(), cVar4 != '\0' || (local_48 == (char *)0x12)) ||
          (local_48 == (char *)0x3)))) goto LAB_00720400;
    }
LAB_0072040a:
    iVar6 = local_50;
    piVar14 = (int *)(local_50 + 0xc);
    if (*(int *)(local_50 + 0xc) != 0) goto LAB_00720515;
    pbVar12 = *(byte **)(local_50 + 0x74);
    local_34 = piVar14;
    if (pbVar12 == (byte *)0x0) {
LAB_00720469:
      cVar4 = FUN_0040a5d0("Closed",1);
      if (cVar4 != '\0') {
        FUN_0040a1b0();
        *(undefined1 *)(iVar6 + 0x84) = 1;
      }
    }
    else {
      pbVar11 = pbVar12;
      if (0xf < *(uint *)(pbVar12 + 0x14)) {
        pbVar11 = *(byte **)pbVar12;
      }
      pcVar17 = "Closed";
      do {
        bVar2 = *pbVar11;
        bVar20 = bVar2 < (byte)*pcVar17;
        if (bVar2 != *pcVar17) {
LAB_00720453:
          uVar5 = -(uint)bVar20 | 1;
          goto LAB_00720458;
        }
        if (bVar2 == 0) break;
        bVar2 = pbVar11[1];
        bVar20 = bVar2 < (byte)pcVar17[1];
        if (bVar2 != pcVar17[1]) goto LAB_00720453;
        pbVar11 = pbVar11 + 2;
        pcVar17 = pcVar17 + 2;
      } while (bVar2 != 0);
      uVar5 = 0;
LAB_00720458:
      if ((uVar5 != 0) || ((pbVar12[0x34] != 0 && (*(char *)(local_50 + 0x84) == '\0'))))
      goto LAB_00720469;
    }
    piVar14 = (int *)(iVar6 + 0xc);
    piVar10 = DAT_00c71678;
  }
  else {
LAB_00720400:
    if ((char)local_34 != '\0') goto LAB_0072040a;
    piVar14 = (int *)(local_50 + 0xc);
LAB_00720515:
    iVar6 = local_50;
    piVar10 = DAT_00c71678;
    local_3c = piVar14;
    local_34 = piVar14;
    if ((*piVar14 != 1) && (DAT_00c71678[0x9961] != 0x1f)) {
      if (*(int *)(local_50 + 0x74) == 0) {
LAB_007205c9:
        pbVar12 = *(byte **)(local_50 + 0x74);
        if (pbVar12 != (byte *)0x0) {
          pbVar11 = pbVar12;
          if (0xf < *(uint *)(pbVar12 + 0x14)) {
            pbVar11 = *(byte **)pbVar12;
          }
          pcVar17 = "Open Animation";
          do {
            bVar2 = *pbVar11;
            bVar20 = bVar2 < (byte)*pcVar17;
            if (bVar2 != *pcVar17) {
LAB_00720600:
              uVar5 = -(uint)bVar20 | 1;
              goto LAB_00720605;
            }
            if (bVar2 == 0) break;
            bVar2 = pbVar11[1];
            bVar20 = bVar2 < (byte)pcVar17[1];
            if (bVar2 != pcVar17[1]) goto LAB_00720600;
            pbVar11 = pbVar11 + 2;
            pcVar17 = pcVar17 + 2;
          } while (bVar2 != 0);
          uVar5 = 0;
LAB_00720605:
          if ((uVar5 == 0) && ((pbVar12[0x34] == 0 || (*(char *)(local_50 + 0x84) != '\0'))))
          goto LAB_00720642;
        }
        cVar4 = FUN_0040a5d0("Open Animation",1);
        if (cVar4 != '\0') {
          FUN_0040a1b0();
          *(undefined1 *)(iVar6 + 0x84) = 1;
        }
      }
      else {
        pbVar12 = *(byte **)(local_50 + 0x74);
        if (*(char *)(local_50 + 0x84) == '\0') {
          if (0xf < *(uint *)(pbVar12 + 0x14)) {
            pbVar12 = *(byte **)pbVar12;
          }
          pcVar17 = "Open Animation";
          do {
            bVar2 = *pbVar12;
            bVar20 = bVar2 < (byte)*pcVar17;
            if (bVar2 != *pcVar17) {
LAB_007205c0:
              uVar5 = -(uint)bVar20 | 1;
              goto joined_r0x007205c7;
            }
            if (bVar2 == 0) break;
            bVar2 = pbVar12[1];
            bVar20 = bVar2 < (byte)pcVar17[1];
            if (bVar2 != pcVar17[1]) goto LAB_007205c0;
            pbVar12 = pbVar12 + 2;
            pcVar17 = pcVar17 + 2;
          } while (bVar2 != 0);
          uVar5 = 0;
        }
        else {
          if (0xf < *(uint *)(pbVar12 + 0x14)) {
            pbVar12 = *(byte **)pbVar12;
          }
          pcVar17 = "Open Animation";
          do {
            bVar2 = *pbVar12;
            bVar20 = bVar2 < (byte)*pcVar17;
            if (bVar2 != *pcVar17) {
LAB_00720580:
              uVar5 = -(uint)bVar20 | 1;
              goto joined_r0x007205c7;
            }
            if (bVar2 == 0) break;
            bVar2 = pbVar12[1];
            bVar20 = bVar2 < (byte)pcVar17[1];
            if (bVar2 != pcVar17[1]) goto LAB_00720580;
            pbVar12 = pbVar12 + 2;
            pcVar17 = pcVar17 + 2;
          } while (bVar2 != 0);
          uVar5 = 0;
        }
joined_r0x007205c7:
        if (uVar5 != 0) goto LAB_007205c9;
      }
LAB_00720642:
      piVar10 = DAT_00c71678;
      if ((*(int *)(iVar6 + 0x74) == 0) || (*(char *)(iVar6 + 0x84) == '\0')) {
LAB_00720701:
        local_2d = '\0';
      }
      else {
        pbVar12 = *(byte **)(iVar6 + 0x74);
        if (0xf < *(uint *)(pbVar12 + 0x14)) {
          pbVar12 = *(byte **)pbVar12;
        }
        pcVar17 = "Open Animation";
        do {
          bVar2 = *pbVar12;
          bVar20 = bVar2 < (byte)*pcVar17;
          if (bVar2 != *pcVar17) {
LAB_00720690:
            uVar5 = -(uint)bVar20 | 1;
            goto LAB_00720695;
          }
          if (bVar2 == 0) break;
          bVar2 = pbVar12[1];
          bVar20 = bVar2 < (byte)pcVar17[1];
          if (bVar2 != pcVar17[1]) goto LAB_00720690;
          pbVar12 = pbVar12 + 2;
          pcVar17 = pcVar17 + 2;
        } while (bVar2 != 0);
        uVar5 = 0;
LAB_00720695:
        if (uVar5 != 0) goto LAB_00720701;
        local_48 = *(char **)(iVar6 + 0x80);
        dVar24 = floor((double)(float)local_48);
        local_48 = (char *)(float)dVar24;
        if ((int)dVar24 != 1) goto LAB_00720701;
        FUN_0040cf50();
        local_54 = 3;
        ppppppcVar13 = local_2c;
        if (0xf < local_18) {
          ppppppcVar13 = (char ******)local_2c[0];
        }
        iVar15 = _strnicmp((char *)ppppppcVar13,"gfx/grid/Door_11_TrapDoor",0x19);
        local_2d = '\x01';
        piVar10 = DAT_00c71678;
        if (iVar15 != 0) goto LAB_00720701;
      }
      if ((local_54 & 1) != 0) {
        if (0xf < local_18) {
          ppppppcVar13 = (char ******)local_2c[0];
          if ((0xfff < local_18 + 1) &&
             (ppppppcVar13 = (char ******)local_2c[0][-1],
             (char *)0x1f < (char *)((int)local_2c[0] + (-4 - (int)ppppppcVar13)))) {
                    /* WARNING: Subroutine does not return */
            _invalid_parameter_noinfo_noreturn();
          }
          FUN_00aef15c(ppppppcVar13);
          piVar10 = DAT_00c71678;
        }
        local_1c = 0;
        local_18 = 0xf;
        local_2c[0] = (char *****)((uint)local_2c[0] & 0xffffff00);
      }
      if (local_2d != '\0') {
        local_54 = 0x395;
        FUN_00956780();
        FUN_0092dc30(local_54,0x3f800000,2,0,0x3f800000,0);
        piVar10 = DAT_00c71678;
      }
      piVar14 = local_3c;
      if ((*(int *)(iVar6 + 0x74) == 0) || (*(char *)(iVar6 + 0x84) == '\0')) {
        local_34 = local_3c;
        *local_3c = 1;
      }
      else {
        local_34 = local_3c;
      }
    }
  }
  if ((((piVar10[0x9a72] == 2) || (piVar10[0x9a72] == 3)) &&
      ((*(byte *)(*(int *)(piVar10[0x60c0] + 4) + 0x44) & 1) == 0)) &&
     (*(int *)(iVar6 + 0x28) <= *(int *)(piVar10[0x60c0] + 0x11f0))) {
    pbVar12 = *(byte **)(iVar6 + 0x74);
    if (pbVar12 == (byte *)0x0) {
LAB_007207ef:
      cVar4 = FUN_0040a5d0("Closed",1);
      piVar10 = DAT_00c71678;
      if (cVar4 != '\0') {
        FUN_0040a1b0();
        *(undefined1 *)(iVar6 + 0x84) = 1;
        piVar10 = DAT_00c71678;
      }
    }
    else {
      pbVar11 = pbVar12;
      if (0xf < *(uint *)(pbVar12 + 0x14)) {
        pbVar11 = *(byte **)pbVar12;
      }
      pcVar17 = "Closed";
      do {
        bVar2 = *pbVar11;
        bVar20 = bVar2 < (byte)*pcVar17;
        if (bVar2 != *pcVar17) {
LAB_007207d1:
          uVar5 = -(uint)bVar20 | 1;
          goto LAB_007207d6;
        }
        if (bVar2 == 0) break;
        bVar2 = pbVar11[1];
        bVar20 = bVar2 < (byte)pcVar17[1];
        if (bVar2 != pcVar17[1]) goto LAB_007207d1;
        pbVar11 = pbVar11 + 2;
        pcVar17 = pcVar17 + 2;
      } while (bVar2 != 0);
      uVar5 = 0;
LAB_007207d6:
      if ((uVar5 != 0) || ((pbVar12[0x34] != 0 && (*(char *)(iVar6 + 0x84) == '\0'))))
      goto LAB_007207ef;
    }
    *local_34 = 0;
    piVar14 = local_34;
  }
  if (*piVar14 == 1) {
    cVar4 = FUN_0074e9b0();
    if ((cVar4 == '\0') || (*(int *)(iVar6 + 0x18) != 0)) {
      pbVar12 = *(byte **)(iVar6 + 0x74);
      if (pbVar12 != (byte *)0x0) {
        pbVar11 = pbVar12;
        if (0xf < *(uint *)(pbVar12 + 0x14)) {
          pbVar11 = *(byte **)pbVar12;
        }
        pcVar17 = "Opened";
        do {
          bVar2 = *pbVar11;
          bVar20 = bVar2 < (byte)*pcVar17;
          if (bVar2 != *pcVar17) {
LAB_007208b0:
            uVar5 = -(uint)bVar20 | 1;
            goto LAB_007208b5;
          }
          if (bVar2 == 0) break;
          bVar2 = pbVar11[1];
          bVar20 = bVar2 < (byte)pcVar17[1];
          if (bVar2 != pcVar17[1]) goto LAB_007208b0;
          pbVar11 = pbVar11 + 2;
          pcVar17 = pcVar17 + 2;
        } while (bVar2 != 0);
        uVar5 = 0;
LAB_007208b5:
        if ((uVar5 == 0) &&
           ((piVar14 = local_34, piVar10 = DAT_00c71678, pbVar12[0x34] == 0 ||
            (*(char *)(iVar6 + 0x84) != '\0')))) goto LAB_007208f1;
      }
      cVar4 = FUN_0040a5d0("Opened",1);
      piVar14 = local_34;
      piVar10 = DAT_00c71678;
      if (cVar4 != '\0') {
        FUN_0040a1b0();
        *(undefined1 *)(iVar6 + 0x84) = 1;
        piVar14 = local_34;
        piVar10 = DAT_00c71678;
      }
    }
    else {
      cVar4 = FUN_0040a5d0("Opened",1);
      piVar14 = local_34;
      piVar10 = DAT_00c71678;
      if (((cVar4 != '\0') && (*(int *)(iVar6 + 0x74) != 0)) &&
         (FUN_00408e00(), piVar14 = local_34, piVar10 = DAT_00c71678, *(int *)(iVar6 + 0x74) != 0))
      {
        *(undefined1 *)(iVar6 + 0x84) = 0;
        piVar10 = DAT_00c71678;
      }
    }
  }
LAB_007208f1:
  fVar18 = local_44;
  fVar21 = DAT_00baa904;
  fVar23 = DAT_00baaa00;
  if ((((local_44 != 0.0) && (local_40 < local_58)) && (*piVar14 == 1)) &&
     (((*(char *)((int)local_44 + 0x1398) == '\0' && (*(char *)((int)local_44 + 0x139a) == '\0')) ||
      ((*(int *)((int)local_44 + 0x1410) != 0 &&
       (*(int *)((int)local_44 + 0x1410) == *(int *)((int)local_44 + 0x1e68))))))) {
    if (local_35 == '\0') {
      if (piVar10[0x60c1] == -0x14) {
        FUN_006fd7c0(0xfffffffe,0xffffffff,2,local_44,0xffffffff);
      }
      else {
        local_40 = 1.47417e-42;
        FUN_00956780();
        FUN_0092dc30(local_40,0x3f800000,2,0,0x3f800000,0);
        if ((*(int *)(DAT_00c71678[0x60c0] + 8) == 0x1b) ||
           (cVar4 = FUN_0074e9b0(), piVar14 = DAT_00c71678, cVar4 != '\0')) {
          piVar10 = DAT_00c71678;
          piVar14 = DAT_00c71678 + 0x9952;
          DAT_00c71678[0x9953] = DAT_00c71678[0x9953] | 0x1000;
          piVar10[0x9952] = *piVar14;
          cVar4 = Level__condition_74f030();
          piVar14 = DAT_00c71678;
          if (cVar4 != '\0') {
            piVar10 = DAT_00c71678 + 0x9952;
            DAT_00c71678[0x9953] = DAT_00c71678[0x9953] | 0x8000;
            piVar14[0x9952] = *piVar10;
          }
        }
        cVar4 = FUN_00665c60();
        if (cVar4 == '\0') {
          if (10 < *piVar14) {
            FUN_004360f0();
            Seeds__advance_stage_slot();
          }
          if (*(int *)(iVar6 + 0x18) == 1) {
            FUN_006fdc10(0,3);
            fVar18 = local_44;
          }
          else {
            iVar15 = FUN_0071f600();
            piVar14 = DAT_00c71678;
            local_2d = iVar15 != 0;
            cVar4 = FUN_0074bac0();
            if ((cVar4 == '\0') ||
               ((extraout_EDX != 2 && ((extraout_EDX != 1 || (local_2d == '\0')))))) {
              local_35 = '\0';
            }
            else {
              local_35 = '\x01';
            }
            cVar4 = FUN_0074bac0();
            if ((cVar4 == '\0') ||
               ((extraout_EDX_00 != 4 && ((extraout_EDX_00 != 3 || (local_2d == '\0')))))) {
              local_2d = '\0';
            }
            else {
              local_2d = '\x01';
            }
            iVar15 = FUN_00706940();
            if (((*(int *)(iVar15 + 0x80) == 2) && (piVar14[0x9961] != 0x2c)) &&
               (((local_35 != '\0' &&
                 (iVar15 = PlayerManager__FirstCollectibleOwner(0x272,piVar14 + 0x6eaa,1),
                 piVar14 = DAT_00c71678, iVar15 == 0)) ||
                ((local_2d != '\0' &&
                 (iVar15 = PlayerManager__FirstCollectibleOwner(0x273,piVar14 + 0x6eaa,1),
                 iVar15 == 0)))))) {
              FUN_006fd7c0(DAT_00c71678[0x60b4],0xffffffff,0x16,local_44,0);
              uVar5 = 0;
              fVar18 = local_44;
              if (DAT_00c71678[0x6eab] - DAT_00c71678[0x6eaa] >> 2 != 0) {
                do {
                  local_48 = (char *)PlayerManager__get_player_417870();
                  piVar14 = DAT_00c71678;
                  if (*(int *)((int)local_48 + 0x2c) == 0) {
                    FUN_007abe20();
                    piVar14 = DAT_00c71678;
                    fVar21 = (float)(*(int *)(iVar6 + 0x24) / *(int *)(DAT_00c71678[0x60c0] + 0xc))
                             * DAT_00baa904 + DAT_00baaa00;
                    *(float *)((int)local_48 + 0x1b1c) =
                         (float)(*(int *)(iVar6 + 0x24) % *(int *)(DAT_00c71678[0x60c0] + 0xc)) *
                         DAT_00baa904 + DAT_00baa904;
                    *(float *)((int)local_48 + 0x1b20) = fVar21;
                  }
                  uVar5 = uVar5 + 1;
                  fVar18 = local_44;
                } while (uVar5 < (uint)(piVar14[0x6eab] - piVar14[0x6eaa] >> 2));
              }
            }
            else {
              FUN_006fdc10(0,0);
              fVar18 = local_44;
            }
          }
        }
        else {
          FUN_006fdc10(1,0);
          fVar18 = local_44;
        }
      }
      FUN_007abe20();
      piVar10 = DAT_00c71678;
      fVar23 = DAT_00baaa00;
      fVar21 = DAT_00baa904;
      fVar22 = (float)(*(int *)(iVar6 + 0x24) / *(int *)(DAT_00c71678[0x60c0] + 0xc)) * DAT_00baa904
               + DAT_00baaa00;
      *(float *)((int)fVar18 + 0x1b1c) =
           (float)(*(int *)(iVar6 + 0x24) % *(int *)(DAT_00c71678[0x60c0] + 0xc)) * DAT_00baa904 +
           DAT_00baa904;
      *(float *)((int)fVar18 + 0x1b20) = fVar22;
    }
    else {
      local_40 = 1.47417e-42;
      FUN_00956780();
      FUN_0092dc30(local_40,0x3f800000,2,0,0x3f800000,0);
      DAT_00c71678[0x60c6] = -1;
      FUN_006fd7c0(0xfffffff6,0xffffffff,0x16,local_44,0xffffffff);
      uVar5 = 0;
      piVar14 = DAT_00c71678 + 0x6eaa;
      piVar10 = DAT_00c71678;
      fVar21 = DAT_00baa904;
      fVar23 = DAT_00baaa00;
      if (DAT_00c71678[0x6eab] - *piVar14 >> 2 != 0) {
        do {
          iVar6 = piVar14[1];
          if (iVar6 - *piVar14 >> 2 == 0) {
            Isaac__log(0x10);
            iVar6 = piVar14[1];
            piVar10 = DAT_00c71678;
          }
          piVar14 = (int *)*piVar14;
          if (uVar5 < (uint)(iVar6 - (int)piVar14 >> 2)) {
            piVar14 = piVar14 + uVar5;
          }
          iVar6 = *piVar14;
          if (*(int *)(iVar6 + 0x2c) == 0) {
            FUN_007abe20();
            piVar10 = DAT_00c71678;
            fVar21 = (float)(*(int *)(local_50 + 0x24) / *(int *)(DAT_00c71678[0x60c0] + 0xc)) *
                     DAT_00baa904 + DAT_00baaa00;
            *(float *)(iVar6 + 0x1b1c) =
                 (float)(*(int *)(local_50 + 0x24) % *(int *)(DAT_00c71678[0x60c0] + 0xc)) *
                 DAT_00baa904 + DAT_00baa904;
            *(float *)(iVar6 + 0x1b20) = fVar21;
          }
          piVar14 = piVar10 + 0x6eaa;
          uVar5 = uVar5 + 1;
          fVar21 = DAT_00baa904;
          fVar23 = DAT_00baaa00;
        } while (uVar5 < (uint)(piVar10[0x6eab] - *piVar14 >> 2));
      }
    }
  }
  iVar6 = local_50;
  pcVar17 = (char *)piVar10[0x60c0];
  local_48 = pcVar17;
  if (((*pcVar17 != '\0') &&
      (piVar10[0x993e] - *(int *)(pcVar17 + 0x11f0) ==
       ((piVar10[0x993e] - *(int *)(pcVar17 + 0x11f0)) / 0xf) * 0xf)) &&
     (((*piVar10 == 9 && (piVar10[0x60c1] == -9)) || (*(int *)(local_50 + 0x18) == 1)))) {
    local_44 = DAT_00baa0d0;
    if (piVar10[0x60c1] == -7) {
      local_44 = DAT_00baa0a0;
    }
    uVar19 = 6;
    if (piVar10[0x60c1] != -7) {
      uVar19 = 0xd;
    }
    if (*local_34 != 1) {
      local_44 = local_44 * DAT_00baa198;
    }
    iVar15 = *(int *)(local_50 + 0x24);
    *(int *)(pcVar17 + 0x70fc) = *(int *)(pcVar17 + 0x70fc) + 1;
    local_48 = (char *)((float)(iVar15 % *(int *)(pcVar17 + 0xc)) * fVar21 + fVar21);
    local_40 = (float)(iVar15 / *(int *)(pcVar17 + 0xc)) * fVar21 + fVar23;
    local_58 = (float)(*(uint *)(pcVar17 + 0x70fc) & 0x80000001);
    if ((int)local_58 < 0) {
      local_58 = (float)(((int)local_58 - 1U | 0xfffffffe) + 1);
    }
    if (1 < (uint)local_58) {
      Isaac__log(0x10);
    }
    iVar15 = (int)local_58 + 0x407;
    *(char **)(pcVar17 + iVar15 * 0x1c) = local_48;
    *(float *)(pcVar17 + iVar15 * 0x1c + 4) = local_40;
    pcVar1 = pcVar17 + iVar15 * 0x1c + 8;
    pcVar1[0] = '\0';
    pcVar1[1] = '\0';
    pcVar1[2] = '\0';
    pcVar1[3] = '\0';
    *(float *)(pcVar17 + iVar15 * 0x1c + 0xc) = local_44;
    pcVar1 = pcVar17 + iVar15 * 0x1c + 0x10;
    pcVar1[0] = -0xc;
    pcVar1[1] = -3;
    pcVar1[2] = 'T';
    pcVar1[3] = '<';
    pcVar1 = pcVar17 + iVar15 * 0x1c + 0x14;
    pcVar1[0] = '\0';
    pcVar1[1] = '\0';
    pcVar1[2] = '\0';
    pcVar1[3] = '\0';
    *(undefined4 *)(pcVar17 + iVar15 * 0x1c + 0x18) = uVar19;
  }
  if (*(char *)(iVar6 + 0x149) != '\0') {
    FUN_00409030();
    FUN_00409030();
  }
  if (local_68[0] == '\0') {
    if (DAT_00c7de78 == 0) {
      puVar9 = &DAT_00c7f618;
    }
    else {
      puVar9 = (uint *)(DAT_00c7de78 + 0x30);
    }
    if (local_64 != 0) {
      uVar16 = *(uint *)(local_64 + -4);
      uVar5 = *puVar9;
      *puVar9 = *puVar9 - uVar16;
      puVar9[1] = puVar9[1] - (uint)(uVar5 < uVar16);
      free((void *)(local_64 + -4));
    }
  }
  ExceptionList = local_10;
  return;
}
