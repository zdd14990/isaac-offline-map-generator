/* Static decompilation only; PE entry point was not executed. */
/* Target: 006fdc10 */
/* Reference: 006e671d */
/* Caller: FUN_006e3940 @ 006e3940 */


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN_006e3940(int *param_1)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  void **ppvVar4;
  char cVar5;
  byte bVar6;
  uint uVar7;
  int iVar8;
  undefined4 uVar9;
  int *piVar10;
  undefined4 *puVar11;
  byte *pbVar12;
  undefined4 uVar13;
  undefined1 *puVar14;
  char *pcVar15;
  int iVar16;
  int extraout_ECX;
  float *pfVar17;
  uint uVar18;
  byte *pbVar19;
  float *pfVar20;
  bool bVar21;
  float fVar22;
  float fVar23;
  float fVar24;
  float fVar25;
  longlong lVar26;
  undefined8 uVar27;
  double dVar28;
  int local_124 [4];
  int local_114;
  int iStack_110;
  int iStack_10c;
  int iStack_108;
  undefined8 local_104;
  int local_fc;
  int *local_f8;
  int *local_f4;
  float *local_f0;
  char local_e9;
  int local_e8;
  undefined8 local_e4;
  float *local_dc;
  int *local_d4;
  float *local_d0;
  float *local_cc;
  float local_c8;
  float *local_c4;
  char local_bd;
  uint local_ac;
  undefined4 local_9c;
  uint local_98;
  int local_94;
  int iStack_90;
  int iStack_8c;
  int iStack_88;
  int local_84;
  int iStack_80;
  int iStack_7c;
  int iStack_78;
  undefined8 local_74;
  int local_6c;
  undefined4 local_68;
  undefined4 uStack_64;
  undefined4 uStack_60;
  undefined4 uStack_5c;
  char *local_54;
  float local_50;
  float local_4c;
  float *local_48;
  float *local_44;
  float *local_40;
  int local_34;
  undefined8 local_30;
  float local_28;
  uint local_24;
  undefined1 *puStack_20;
  void *local_1c;
  undefined1 *puStack_18;
  undefined4 local_14;

  puStack_20 = &stack0xfffffffc;
  local_14 = 0xffffffff;
  puStack_18 = &LAB_00afb109;
  local_1c = ExceptionList;
  uVar7 = DAT_00bf93b4 ^ (uint)&stack0xfffffff0;
  ppvVar4 = &local_1c;
  if (0 < param_1[0x155]) {
    if (param_1[0x62] == 0) {
      param_1[0x155] = param_1[0x155] + -1;
      return;
    }
    ExceptionList = &local_1c;
    param_1[0x155] = 0;
    ppvVar4 = ExceptionList;
  }
  ExceptionList = ppvVar4;
  fVar24 = DAT_00baae30;
  fVar22 = (float)param_1[0x1b9];
  local_f8 = param_1;
  local_24 = uVar7;
  if ((fVar22 < 0.0) ||
     (puVar14 = &stack0xfffffffc, (float)param_1[0x1ba] <= 0.0 && (float)param_1[0x1ba] != 0.0)) {
    iVar8 = 4;
    fVar25 = (float)param_1[0x1ba];
    fVar23 = (float)param_1[0xe7] * DAT_00baa4b0;
    if (fVar22 < DAT_00baae30) {
      iVar8 = 0;
    }
    param_1[0x62] = iVar8;
    iVar8 = 6;
    if (fVar22 < fVar24) {
      iVar8 = 3;
    }
    param_1[0x61] = iVar8;
    param_1[0x1ba] = (int)(fVar23 + fVar25);
    param_1[0x1b9] = (int)((float)param_1[0xe7] * fVar25 + fVar22);
    puVar14 = &stack0xfffffffc;
    if ((((((char)param_1[100] != '\0') &&
          (cVar5 = FUN_006ee340(uVar7), puVar14 = puStack_20, cVar5 != '\0')) && (param_1[0xc] != 0)
         ) && (cVar5 = FUN_006e6e40(), puVar14 = puStack_20, cVar5 != '\0')) &&
       ((iVar8 = *(int *)(*(int *)(DAT_00c71678 + 0x18300) + 8), iVar8 == 0xb || (iVar8 == 0x11))))
    {
      FUN_00833420();
      puVar14 = puStack_20;
    }
    puStack_20 = puVar14;
    puVar14 = puStack_20;
    if (DAT_00ba9fe4 <= (float)param_1[0x1b9]) {
      param_1[0x5b] = param_1[0x5b] & 0xfbffffff;
      param_1[0x1b9] = 0;
      param_1[0x1ba] = 0;
      param_1[0x5a] = param_1[0x5a];
      param_1[0x62] = 4;
      param_1[0x61] = 5;
      cVar5 = FUN_006ee340(uVar7);
      puVar14 = puStack_20;
      if (((cVar5 != '\0') && (param_1[0xc] != 0)) &&
         ((cVar5 = FUN_006e6e40(), puVar14 = puStack_20, cVar5 != '\0' &&
          ((iVar8 = *(int *)(*(int *)(DAT_00c71678 + 0x18300) + 8), iVar8 == 0xb || (iVar8 == 0x11))
          )))) {
        FUN_00833420();
        puVar14 = puStack_20;
      }
    }
  }
  puStack_20 = puVar14;
  iVar8 = param_1[0xb];
  cVar5 = FUN_006ee340(uVar7);
  if (((cVar5 != '\0') && (param_1[0xd4] = param_1[0x1b9], param_1[0xef] != 0)) &&
     ((param_1[0x5b] & 0x2000000U) != 0)) {
    fVar22 = *(float *)(param_1[0xef] + 0x340);
    param_1[0xd8] = (int)(*(float *)(param_1[0xef] + 0x33c) - (float)param_1[0xcf]);
    param_1[0xd9] = (int)(fVar22 - (float)param_1[0xd0]);
    iVar8 = param_1[0xb];
  }
  if (iVar8 == 100) {
    if ((param_1[0x5a] & 4U) != 0) {
      uVar9 = FUN_006eef60();
      piVar10 = (int *)FUN_00428b20(1000,0xf,param_1 + 0xcf,&DAT_00c7b640,0,0,uVar9);
      (**(code **)(*piVar10 + 0xc))();
      param_1[0x5a] = param_1[0x5a] & 0xfffffffb;
      param_1[0x5b] = param_1[0x5b];
      iVar8 = FUN_00708250();
      if (1 < iVar8) {
        uVar9 = FUN_006eef60();
        local_cc = (float *)FUN_00428b20(1000,0xf,param_1 + 0xcf,&DAT_00c7b640,0,0,uVar9);
        local_44 = (float *)0x0;
        local_d0 = local_cc + 0x12;
        local_40 = (float *)0xf;
        local_54 = (char *)0x0;
        local_54 = (char *)FUN_0040cf00();
        uVar2 = s_gfx_promo_gfuel_effects_explosio_00b67908._12_4_;
        uVar13 = s_gfx_promo_gfuel_effects_explosio_00b67908._8_4_;
        uVar9 = s_gfx_promo_gfuel_effects_explosio_00b67908._4_4_;
        local_44 = (float *)&DAT_00000027;
        local_40 = (float *)&DAT_0000002f;
        *(undefined4 *)local_54 = s_gfx_promo_gfuel_effects_explosio_00b67908._0_4_;
        *(undefined4 *)(local_54 + 4) = uVar9;
        *(undefined4 *)(local_54 + 8) = uVar13;
        *(undefined4 *)(local_54 + 0xc) = uVar2;
        uVar2 = s_gfx_promo_gfuel_effects_explosio_00b67908._28_4_;
        uVar13 = s_gfx_promo_gfuel_effects_explosio_00b67908._24_4_;
        uVar9 = s_gfx_promo_gfuel_effects_explosio_00b67908._20_4_;
        *(undefined4 *)(local_54 + 0x10) = s_gfx_promo_gfuel_effects_explosio_00b67908._16_4_;
        *(undefined4 *)(local_54 + 0x14) = uVar9;
        *(undefined4 *)(local_54 + 0x18) = uVar13;
        *(undefined4 *)(local_54 + 0x1c) = uVar2;
        *(undefined4 *)(local_54 + 0x20) = s_gfx_promo_gfuel_effects_explosio_00b67908._32_4_;
        *(undefined2 *)(local_54 + 0x24) = s_gfx_promo_gfuel_effects_explosio_00b67908._36_2_;
        local_54[0x26] = s_gfx_promo_gfuel_effects_explosio_00b67908[0x26];
        local_54[0x27] = '\0';
        local_14 = 0;
        FUN_0040bd50(&local_54,1);
        local_14 = 0xffffffff;
        if (&DAT_0000000f < local_40) {
          pfVar17 = (float *)((int)local_40 + 1);
          pcVar15 = local_54;
          if ((float *)0xfff < pfVar17) {
            pcVar15 = *(char **)(local_54 + -4);
            pfVar17 = local_40 + 9;
            if ((char *)0x1f < local_54 + (-4 - (int)pcVar15)) {
                    /* WARNING: Subroutine does not return */
              _invalid_parameter_noinfo_noreturn();
            }
          }
          FUN_00aef15c(pcVar15,pfVar17);
        }
        iVar8 = FUN_006eef60();
        local_dc = (float *)0x33d;
        local_c4 = (float *)((float)((double)iVar8 + (double)(&DAT_00bacb00)[-(iVar8 >> 0x1f)]) *
                             DAT_00ba9ff4 * DAT_00baa198 + DAT_00baa3e0);
        FUN_00956780();
        FUN_0092dc30(local_dc,0x3f800000,2,0,local_c4,0);
        FUN_00703670();
        bVar6 = FUN_006eef60();
        pfVar20 = local_cc;
        *(byte *)(local_cc + 0x52) = (bVar6 ^ 0xff) & 1;
        pfVar17 = local_cc + 0x18;
        if (0xf < (uint)local_cc[0x1d]) {
          pfVar17 = (float *)*pfVar17;
        }
        cVar5 = FUN_0040a5d0(pfVar17,1);
        pfVar17 = local_d0;
        if (cVar5 != '\0') {
          FUN_0040a1b0();
          *(undefined1 *)(pfVar17 + 0x11) = 1;
          pfVar20 = local_cc;
        }
        (**(code **)((int)*pfVar20 + 0xc))();
      }
    }
    if (((*(char *)((int)param_1 + 0x171) == '\0') && (param_1[0x62] != 0)) &&
       (param_1[0x171] = param_1[0x171] + 1, 3 < param_1[0x171])) {
      *(undefined1 *)((int)param_1 + 0x171) = 1;
    }
    if (((param_1[0x172] == 0) || (param_1[0xb] != 100)) ||
       (iVar8 = PlayerManager__FirstCollectibleOwner(0x2c7,DAT_00c71678 + 0x1baa8,1), iVar8 == 0)) {
      cVar5 = '\0';
    }
    else {
      cVar5 = '\x01';
    }
    if (cVar5 != *(char *)((int)param_1 + 0x6d9)) {
      if (cVar5 == '\0') {
        FUN_00407f10();
      }
      else {
        FUN_00407690(param_1 + 0x12);
        FUN_00407e90();
        if ((*(int *)(DAT_00c71678 + 0x1830c) == 2) ||
           ((uVar7 = FUN_00748490(), (uVar7 & 0x40) == 0 &&
            (*(char *)((int)param_1 + 0x52e) == '\0')))) {
          uVar9 = 0;
        }
        else {
          uVar9 = 1;
        }
        FUN_006e1e90(*(undefined4 *)(param_1[0x172] + 8),*(undefined4 *)(param_1[0x172] + 0x34),
                     uVar9);
        FUN_0040c000();
        puVar11 = (undefined4 *)FUN_00452bf0();
        local_14 = 1;
        if (0xf < (uint)puVar11[5]) {
          puVar11 = (undefined4 *)*puVar11;
        }
        cVar5 = FUN_0040a5d0(puVar11,1);
        if (cVar5 != '\0') {
          FUN_0040a1b0();
          *(undefined1 *)(param_1 + 0x185) = 1;
        }
        local_14 = 0xffffffff;
        if (0xf < local_98) {
          uVar18 = local_98 + 1;
          uVar7 = local_ac;
          if (0xfff < uVar18) {
            uVar7 = *(uint *)(local_ac - 4);
            uVar18 = local_98 + 0x24;
            if (0x1f < (local_ac - uVar7) - 4) {
                    /* WARNING: Subroutine does not return */
              _invalid_parameter_noinfo_noreturn();
            }
          }
          FUN_00aef15c(uVar7,uVar18);
        }
        local_9c = 0;
        local_98 = 0xf;
        local_ac = local_ac & 0xffffff00;
      }
    }
    if (*(char *)((int)param_1 + 0x6d9) != '\0') {
      FUN_00409030();
      FUN_00409030();
    }
  }
  if ((param_1[0x14d] == 0) && (param_1[0xb] == 10)) {
    local_cc = (float *)0x0;
    local_d0 = (float *)0x0;
    pfVar17 = (float *)0x0;
    local_48 = (float *)0x0;
    local_44 = (float *)0x0;
    local_f0 = (float *)0x0;
    local_40 = (float *)0x0;
    local_14 = 2;
    local_dc = (float *)0x0;
    pfVar20 = local_f0;
    if (*(int *)(DAT_00c71678 + 0x1baac) - *(int *)(DAT_00c71678 + 0x1baa8) >> 2 != 0) {
      pfVar20 = (float *)0x0;
      do {
        local_c4 = (float *)PlayerManager__get_player_417870();
        if (local_c4[0xb] == 0.0) {
          local_cc = (float *)((int)local_cc + 1);
          if ((local_c4[0x4f0] == 1.96182e-44) || (local_c4[0x4f0] == 4.62428e-44)) {
            if (pfVar17 == pfVar20) {
              FUN_0042c920(pfVar17,&local_c4);
              pfVar17 = local_44;
              pfVar20 = local_40;
            }
            else {
              *pfVar17 = (float)local_c4;
              local_44 = pfVar17 + 1;
              pfVar17 = local_44;
            }
          }
        }
        local_dc = (float *)((int)local_dc + 1);
        param_1 = local_f8;
      } while (local_dc <
               (float *)(*(int *)(DAT_00c71678 + 0x1baac) - *(int *)(DAT_00c71678 + 0x1baa8) >> 2));
    }
    local_f0 = pfVar20;
    local_d0 = local_48;
    if (((float *)((int)pfVar17 - (int)local_48 >> 2) == local_cc) && (param_1[0xc] != 7)) {
      local_34 = param_1[0xfb];
      local_30 = DAT_00b1f5ac;
      local_28 = DAT_00b1f5b4;
      iVar8 = RNG__RandomInt();
      pfVar17 = local_d0;
      local_c4 = (float *)local_d0[iVar8];
      if (local_c4 != (float *)0x0) {
        (**(code **)(*param_1 + 0x28))();
        switch(param_1[0xc]) {
        case 1:
        case 8:
        case 9:
        case 10:
        case 0xc:
          uVar9 = 2;
          break;
        default:
          uVar9 = 1;
          break;
        case 3:
          uVar9 = 3;
          break;
        case 4:
          uVar9 = 5;
          break;
        case 5:
        case 6:
        case 0xb:
          uVar9 = 4;
          break;
        case 7:
          uVar9 = 6;
        }
        FUN_007599d0(uVar9,param_1 + 0xcf,0);
        if (pfVar17 == (float *)0x0) {
          ExceptionList = local_1c;
          return;
        }
        uVar7 = (int)local_f0 - (int)pfVar17 & 0xfffffffc;
        pfVar20 = pfVar17;
        if (uVar7 < 0x1000) {
LAB_006e4146:
          FUN_00aef15c(pfVar20,uVar7);
          ExceptionList = local_1c;
          return;
        }
        pfVar20 = (float *)pfVar17[-1];
        uVar7 = uVar7 + 0x23;
        if ((undefined1 *)((int)pfVar17 + (-4 - (int)pfVar20)) < (undefined1 *)0x20)
        goto LAB_006e4146;
        goto LAB_006e4192;
      }
    }
    local_14 = 0xffffffff;
    if (local_d0 != (float *)0x0) {
      uVar7 = ((int)local_f0 - (int)local_d0 >> 2) * 4;
      pfVar17 = local_d0;
      if (0xfff < uVar7) {
        pfVar17 = (float *)local_d0[-1];
        uVar7 = uVar7 + 0x23;
        if ((undefined1 *)0x1f < (undefined1 *)((int)local_d0 + (-4 - (int)pfVar17))) {
LAB_006e4192:
                    /* WARNING: Subroutine does not return */
          _invalid_parameter_noinfo_noreturn();
        }
      }
      FUN_00aef15c(pfVar17,uVar7);
    }
  }
  iVar8 = PlayerManager__FirstCollectibleOwner(0x1a8,DAT_00c71678 + 0x1baa8,1);
  if ((iVar8 != 0) && (param_1[0x14d] == 0)) {
    iVar8 = param_1[0xd];
    if (iVar8 == 5) {
      bVar21 = param_1[0xe] == 0x45;
    }
    else {
      if (iVar8 == 1) goto LAB_006e4283;
      bVar21 = iVar8 == 3;
    }
    if ((!bVar21) &&
       ((((iVar8 = param_1[0xb], iVar8 == 0x1e || (iVar8 == 0x28)) || (iVar8 == 0x14)) ||
        ((iVar8 == 0x5a || (iVar8 == 300)))))) {
      iVar8 = RNG__RandomInt();
      if (iVar8 == 0) {
        (**(code **)(*param_1 + 0x28))();
        uVar9 = RNG__Next();
        iVar8 = FUN_00428b20(5,0x45,param_1 + 0xcf,param_1 + 0xd8,0,0,uVar9);
        *(int *)(iVar8 + 0x528) = param_1[0x14a];
        ExceptionList = local_1c;
        return;
      }
      param_1[0xd] = 5;
      param_1[0xe] = 0x45;
    }
  }
LAB_006e4283:
  if (param_1[0xb] == 0x28) {
    iVar8 = param_1[0xc];
    if (iVar8 == 3) {
      uVar9 = FUN_006eef60();
      FUN_00428b20(4,3,param_1 + 0xcf,&DAT_00c7b640,0,0,uVar9);
      goto LAB_006e42ba;
    }
    if (iVar8 == 5) {
      uVar9 = FUN_006eef60();
      FUN_00428b20(4,4,param_1 + 0xcf,&DAT_00c7b640,0,0,uVar9);
      (**(code **)(*param_1 + 0x28))();
      ExceptionList = local_1c;
      return;
    }
    if (iVar8 == 6) {
      uVar9 = FUN_006eef60();
      FUN_00428b20(4,0x12,param_1 + 0xcf,&DAT_00c7b640,0,0,uVar9);
      (**(code **)(*param_1 + 0x28))();
      ExceptionList = local_1c;
      return;
    }
    if ((param_1[0xd] == 4) &&
       ((((iVar8 = param_1[0xe], iVar8 == 3 || (iVar8 == 4)) || (iVar8 == 0x12)) &&
        ((param_1[0x1f] != 0 && ((char)param_1[0x23] != '\0')))))) {
      pbVar12 = (byte *)param_1[0x1f];
      if (0xf < *(uint *)(pbVar12 + 0x14)) {
        pbVar12 = *(byte **)pbVar12;
      }
      pcVar15 = "Appear";
      do {
        bVar6 = *pbVar12;
        bVar21 = bVar6 < (byte)*pcVar15;
        if (bVar6 != *pcVar15) {
LAB_006e4390:
          uVar7 = -(uint)bVar21 | 1;
          goto LAB_006e4395;
        }
        if (bVar6 == 0) break;
        bVar6 = pbVar12[1];
        bVar21 = bVar6 < (byte)pcVar15[1];
        if (bVar6 != pcVar15[1]) goto LAB_006e4390;
        pbVar12 = pbVar12 + 2;
        pcVar15 = pcVar15 + 2;
      } while (bVar6 != 0);
      uVar7 = 0;
LAB_006e4395:
      if (uVar7 == 0) {
        FUN_0040a380(&DAT_00b1bc54,0);
        param_1[0x62] = 4;
      }
    }
  }
  pfVar17 = (float *)(param_1 + 0xcd);
  if (((float)param_1[0xcd] == DAT_00c7b640) && ((float)param_1[0xce] == DAT_00c7b644)) {
    *pfVar17 = (float)param_1[0xcf];
    param_1[0xce] = param_1[0xd0];
    if (param_1[0xb] == 100) {
      local_c4 = *(float **)(DAT_00c71678 + 0x18300);
      iVar8 = FUN_00812c90();
      if (-1 < iVar8) {
        lVar26 = FUN_00435c70();
        if ((lVar26 < 0x1c000000000) &&
           ((int *)local_c4[(int)((ulonglong)lVar26 >> 0x20) + 9] != (int *)0x0)) {
          (**(code **)(*(int *)local_c4[(int)((ulonglong)lVar26 >> 0x20) + 9] + 0x14))
                    (0,(int)lVar26);
        }
      }
    }
  }
  if (param_1[0x154] == 2) {
    *pfVar17 = (float)param_1[0xcf];
    param_1[0xce] = param_1[0xd0];
    param_1[0x154] = 0;
  }
  iVar8 = param_1[0xb];
  if (iVar8 == 100) {
    iVar8 = param_1[0x165];
    if (iVar8 != 0) {
      *pfVar17 = *(float *)(iVar8 + 0x334);
      param_1[0xce] = *(int *)(iVar8 + 0x338);
      iVar16 = param_1[0x165];
      iVar8 = *(int *)(iVar16 + 0x364);
      param_1[0xd8] = *(int *)(iVar16 + 0x360);
      param_1[0xd9] = iVar8;
      iVar8 = *(int *)(iVar16 + 0x340);
      param_1[0xcf] = *(int *)(iVar16 + 0x33c);
      param_1[0xd0] = iVar8;
      goto LAB_006e45ad;
    }
LAB_006e4506:
    local_c4 = *(float **)(DAT_00c71678 + 0x18300);
    if ((local_c4[2] != 2.24208e-44) && (*(int *)(DAT_00c71678 + 0x264f8) - param_1[0xca] < 6)) {
      local_e4 = CONCAT44(*pfVar17,(undefined4)local_e4);
      local_dc = (float *)param_1[0xce];
      iVar8 = FUN_007f0780(*pfVar17,local_dc);
      if (iVar8 != 0) {
        pfVar20 = (float *)FUN_00813520(&local_44,pfVar17,0x42200000,1,0,0);
        *pfVar17 = *pfVar20;
        param_1[0xce] = (int)pfVar20[1];
      }
    }
    param_1[0xd8] = (int)(*pfVar17 - (float)param_1[0xcf]);
    param_1[0xd9] = (int)((float)param_1[0xce] - (float)param_1[0xd0]);
  }
  else {
    if ((param_1[0x14d] != 0) || (iVar8 == 0x17c)) goto LAB_006e4506;
    if (iVar8 == 0x14) {
      if (param_1[0xc] == 6) goto LAB_006e4506;
    }
    else if ((iVar8 == 0x186) || (iVar8 == 0x39)) goto LAB_006e4506;
  }
LAB_006e45ad:
  if (param_1[0x154] == 1) {
    local_c4 = (float *)(param_1 + 0xcf);
    iVar8 = FUN_00703950();
    iVar16 = 0;
    local_d0 = *(float **)(DAT_00c71678 + 0x18300);
    do {
      if (local_d0[iVar16 + 0x1c9] != 0.0) {
        local_dc = *(float **)((int)local_d0[iVar16 + 0x1c9] + 0x24);
        local_cc = (float *)local_d0[3];
        fVar22 = ((float)((int)local_dc / (int)local_cc) * DAT_00baa904 + DAT_00baaa00) -
                 *(float *)(iVar8 + 0x340);
        fVar24 = ((float)((int)local_dc % (int)local_cc) * DAT_00baa904 + DAT_00baa904) -
                 *(float *)(iVar8 + 0x33c);
        if (fVar22 * fVar22 + fVar24 * fVar24 < DAT_00baac18) {
          if (-1 < iVar16) {
            local_f0 = (float *)(*local_c4 - *(float *)(iVar8 + 0x33c));
            local_d0 = (float *)(local_c4[1] - *(float *)(iVar8 + 0x340));
            fVar22 = (float)local_f0 * (float)local_f0 + (float)local_d0 * (float)local_d0;
            FUN_00435a50();
            if (DAT_00ba9fe4 < fVar22) {
              local_f0 = (float *)((float)local_f0 * (DAT_00baa6fc / fVar22));
              local_d0 = (float *)((float)local_d0 * (DAT_00baa6fc / fVar22));
            }
            pfVar17 = (float *)(*local_c4 -
                               ((float)((int)local_dc % (int)local_cc) * DAT_00baa904 + DAT_00baa904
                               ));
            local_dc = (float *)(local_c4[1] -
                                ((float)((int)local_dc / (int)local_cc) * DAT_00baa904 +
                                DAT_00baaa00));
            fVar22 = (float)local_dc * (float)local_dc + (float)pfVar17 * (float)pfVar17;
            local_c4 = pfVar17;
            FUN_00435a50();
            pfVar20 = local_dc;
            pfVar17 = local_c4;
            if (DAT_00ba9fe4 < fVar22) {
              pfVar20 = (float *)((DAT_00baa784 / fVar22) * (float)local_dc);
              pfVar17 = (float *)((float)local_c4 * (DAT_00baa784 / fVar22));
            }
            param_1[0xd8] = (int)((float)local_f0 + (float)pfVar17 + (float)param_1[0xd8]);
            param_1[0xd9] = (int)((float)local_d0 + (float)pfVar20 + (float)param_1[0xd9]);
          }
          break;
        }
      }
      iVar16 = iVar16 + 1;
    } while (iVar16 < 8);
    param_1[0x154] = 2;
  }
  if (param_1[0xb] == 0x17c) {
    param_1[0xd5] = -3000;
  }
  else if ((((param_1[0xb] == 10) && (param_1[0xc] == 9)) && (param_1[0x14d] == 0)) &&
          (*(char *)((int)param_1 + 0x173) == '\0')) {
    iVar8 = FUN_00703950();
    local_d0 = (float *)((*(float *)(iVar8 + 0x360) + *(float *)(iVar8 + 0x360) +
                         *(float *)(iVar8 + 0x33c)) - (float)param_1[0xcf]);
    local_f0 = (float *)((*(float *)(iVar8 + 0x364) + *(float *)(iVar8 + 0x364) +
                         *(float *)(iVar8 + 0x340)) - (float)param_1[0xd0]);
    FUN_0041a790(&local_34,param_1 + 0xcf,1);
    fVar22 = 0.0;
    local_14 = 3;
    if (local_28 != 0.0) {
      do {
        iVar8 = *(int *)((int)local_30 + (int)fVar22 * 4);
        if ((*(int *)(iVar8 + 0x28) == 3) &&
           ((*(int *)(iVar8 + 0x2c) == 0x40 || (*(int *)(iVar8 + 0x2c) == 0x66)))) {
          pfVar17 = (float *)((*(float *)(iVar8 + 0x360) + *(float *)(iVar8 + 0x360) +
                              *(float *)(iVar8 + 0x33c)) - (float)param_1[0xcf]);
          pfVar20 = (float *)((*(float *)(iVar8 + 0x364) + *(float *)(iVar8 + 0x364) +
                              *(float *)(iVar8 + 0x340)) - (float)param_1[0xd0]);
          if ((float)pfVar20 * (float)pfVar20 + (float)pfVar17 * (float)pfVar17 <
              (float)local_d0 * (float)local_d0 + (float)local_f0 * (float)local_f0) {
            local_f0 = pfVar20;
            local_d0 = pfVar17;
          }
        }
        fVar22 = (float)((int)fVar22 + 1);
      } while ((uint)fVar22 < (uint)local_28);
    }
    local_c4 = (float *)((float)local_d0 * (float)local_d0 + (float)local_f0 * (float)local_f0);
    if (DAT_00baabf0 <= (float)local_c4) {
      if ((((float)param_1[0xd8] * (float)param_1[0xd8] +
            (float)param_1[0xd9] * (float)param_1[0xd9] <= DAT_00baa75c) && (param_1[0x1f] != 0)) &&
         (*(char *)(param_1[0x1f] + 0x34) != '\0')) {
        uVar27 = 0xb1bc54;
        goto LAB_006e4bf6;
      }
    }
    else {
      local_e4 = DAT_00b1f66c;
      local_e8 = param_1[0xfb] * ((*(int *)(DAT_00c71678 + 0x264f8) - param_1[0xca]) / 10);
      if (local_e8 == 0) {
        local_e8 = 1;
      }
      local_dc = (float *)DAT_00b1f674;
      RNG__Next();
      local_dc = (float *)((float)((double)local_e8 + (double)(&DAT_00bacb00)[-(local_e8 >> 0x1f)])
                           * DAT_00ba9ff0 * DAT_00baaa78 - DAT_00baa9b4);
      local_cc = (float *)(((float)local_c4 * DAT_00baa6fc) / DAT_00baabf0);
      FUN_00435a50();
      if ((float)local_c4 <= DAT_00ba9fe4) {
        local_c4 = local_d0;
        local_cc = local_f0;
      }
      else {
        fVar22 = (float)local_cc / (float)local_c4;
        local_c4 = (float *)(fVar22 * (float)local_d0);
        local_cc = (float *)(fVar22 * (float)local_f0);
      }
      pfVar20 = (float *)((float)local_dc * DAT_00baa088);
      local_dc = pfVar20;
      FUN_0041d540();
      pfVar17 = local_dc;
      local_d0 = pfVar20;
      FUN_0041d520();
      fVar22 = (float)param_1[0xdb];
      fVar24 = (float)((uint)((float)local_d0 * (float)local_c4 - (float)pfVar17 * (float)local_cc)
                      ^ DAT_00bacb70);
      if (fVar22 != DAT_00ba9fe4) {
        param_1[0xd9] =
             (int)(((float)param_1[0xe7] *
                   (float)((uint)((float)pfVar17 * (float)local_c4 +
                                 (float)local_d0 * (float)local_cc) ^ DAT_00bacb70)) / fVar22 +
                  (float)param_1[0xd9]);
        param_1[0xd8] = (int)(((float)param_1[0xe7] * fVar24) / fVar22 + (float)param_1[0xd8]);
      }
      if (param_1[0x62] != 0) {
        uVar27 = 0xb67980;
LAB_006e4bf6:
        FUN_0040a380(uVar27);
      }
    }
    local_14 = 0xffffffff;
    if ((char)local_34 == '\0') {
      local_14 = 4;
      FUN_00a648b0(0,0);
      local_14 = 0xffffffff;
    }
  }
  if ((((param_1[0xb] == 100) && (param_1[0xc] == 0x226)) && ((char)param_1[0x14b] != '\0')) &&
     ((**(char **)(DAT_00c71678 + 0x18300) != '\0' &&
      (*(int *)(DAT_00c71678 + 0x264f8) - *(int *)(*(char **)(DAT_00c71678 + 0x18300) + 0x11f0) == 4
      )))) {
    uVar9 = FUN_006eef60();
    local_c8 = (float)param_1[0xcf] + DAT_00ba9fe4;
    local_c4 = (float *)((float)param_1[0xd0] + DAT_00baa81c);
    FUN_00428b20(1000,0xf,&local_c8,&DAT_00c7b640,0,0,uVar9);
    uVar27 = FUN_00435a80();
    (*(code *)((ulonglong)uVar27 >> 0x20))((int)uVar27,0xffffffff,0xff,0,1);
    param_1[0x150] = 4;
    param_1[0x62] = 0;
  }
  FUN_006ae820();
  cVar5 = FUN_006ee340();
  fVar22 = DAT_00baa3a4;
  if (cVar5 == '\0') {
    if ((extraout_ECX == 0x154) || (extraout_ECX == 0x172)) {
      param_1[0xd8] = (int)((float)param_1[0xd8] * DAT_00baa304);
      param_1[0xd9] = (int)((float)param_1[0xd9] * DAT_00baa304);
      fVar24 = (float)param_1[0xce] - (float)param_1[0xd0];
      param_1[0xdd] = 0x40000000;
      param_1[0xde] = 0x3f800000;
      param_1[0xd8] = (int)((float)param_1[0xcd] - (float)param_1[0xcf]);
      goto LAB_006e4deb;
    }
  }
  else if ((param_1[0x5b] & 0x4000000U) == 0) {
    param_1[0xd8] = (int)((float)param_1[0xd8] * DAT_00baa3a4);
    fVar24 = (float)param_1[0xd9] * fVar22;
LAB_006e4deb:
    param_1[0xd9] = (int)fVar24;
  }
  if (param_1[0xb] == 100) {
    param_1[0xdf] = 0x41000000;
    param_1[0xdb] = (int)((float)param_1[0xdb] * fVar22);
    FUN_006edfa0();
  }
  else if ((param_1[0x5b] & 0x4000000U) == 0) {
    param_1[0xdb] = (int)((float)param_1[0xdb] * _DAT_00baa434);
  }
  FUN_006ed690();
  if (((char)param_1[0x14e] != '\0') && (param_1[0x14d] != 0)) {
    local_c8 = (float)param_1[0xcf];
    local_c4 = (float *)param_1[0xd0];
    uVar9 = FUN_00703ab0(&local_c8,1,0,0);
    uVar13 = FUN_008151e0(param_1[0xb],param_1[0xc],param_1[0x14f],uVar9);
    iVar8 = FUN_00816250(param_1[0x14f],uVar13,uVar9);
    if (param_1[0x14d] != iVar8) {
      FUN_006e2570();
    }
  }
  local_bd = FUN_006ee340();
  local_e9 = *(char *)((int)param_1 + 0x173);
  if ((param_1[0x5b] & 0x100U) == 0) {
    if ((local_e9 == '\0') || ((param_1[0x1f] != 0 && ((char)param_1[0x23] != '\0')))) {
      if (param_1[0x1f] != 0) {
        if ((char)param_1[0x23] == '\0') {
          pbVar12 = (byte *)param_1[0x1f];
          if (0xf < *(uint *)(pbVar12 + 0x14)) {
            pbVar12 = *(byte **)pbVar12;
          }
          pcVar15 = "Appear";
          do {
            bVar6 = *pbVar12;
            bVar21 = bVar6 < (byte)*pcVar15;
            if (bVar6 != *pcVar15) {
LAB_006e52d2:
              uVar7 = -(uint)bVar21 | 1;
              goto LAB_006e52d7;
            }
            if (bVar6 == 0) break;
            bVar6 = pbVar12[1];
            bVar21 = bVar6 < (byte)pcVar15[1];
            if (bVar6 != pcVar15[1]) goto LAB_006e52d2;
            pbVar12 = pbVar12 + 2;
            pcVar15 = pcVar15 + 2;
          } while (bVar6 != 0);
          uVar7 = 0;
LAB_006e52d7:
          if (uVar7 != 0) {
            if ((char)param_1[0x23] != '\0') goto LAB_006e5393;
            uVar27 = FUN_00407380();
            do {
              pbVar19 = (byte *)((ulonglong)uVar27 >> 0x20);
              pbVar12 = (byte *)uVar27;
              bVar6 = *pbVar12;
              bVar21 = bVar6 < *pbVar19;
              if (bVar6 != *pbVar19) {
LAB_006e5320:
                uVar7 = -(uint)bVar21 | 1;
                goto LAB_006e5325;
              }
              if (bVar6 == 0) break;
              bVar6 = pbVar12[1];
              bVar21 = bVar6 < pbVar19[1];
              if (bVar6 != pbVar19[1]) goto LAB_006e5320;
              uVar27 = CONCAT44(pbVar19 + 2,pbVar12 + 2);
            } while (bVar6 != 0);
            uVar7 = 0;
LAB_006e5325:
            if (uVar7 != 0) {
              uVar27 = FUN_00407380();
              do {
                pbVar19 = (byte *)((ulonglong)uVar27 >> 0x20);
                pbVar12 = (byte *)uVar27;
                bVar6 = *pbVar12;
                bVar21 = bVar6 < *pbVar19;
                if (bVar6 != *pbVar19) {
LAB_006e5356:
                  uVar7 = -(uint)bVar21 | 1;
                  goto LAB_006e535b;
                }
                if (bVar6 == 0) break;
                bVar6 = pbVar12[1];
                bVar21 = bVar6 < pbVar19[1];
                if (bVar6 != pbVar19[1]) goto LAB_006e5356;
                uVar27 = CONCAT44(pbVar19 + 2,pbVar12 + 2);
              } while (bVar6 != 0);
              uVar7 = 0;
LAB_006e535b:
              if (uVar7 != 0) goto LAB_006e5393;
            }
          }
          if ((local_bd == '\0') || (param_1[0xc] != 0)) {
            FUN_0040a380(&DAT_00b1bc54,0);
LAB_006e53e7:
            param_1[0x62] = 4;
            if (param_1[0xb] == 0x29) {
              param_1[0x61] = 5;
            }
          }
          else {
            FUN_0040a380("Opened",0);
          }
        }
        else {
LAB_006e5393:
          cVar5 = FUN_0040add0();
          if (((cVar5 != '\0') && (FUN_006e7be0(), local_bd == '\0')) &&
             ((cVar5 = FUN_0040a4d0(), cVar5 != '\0' ||
              ((cVar5 = FUN_0040a4d0(), cVar5 != '\0' || (cVar5 = FUN_0040a4d0(), cVar5 != '\0')))))
             ) goto LAB_006e53e7;
        }
      }
    }
    else {
      (**(code **)(*param_1 + 0x28))();
    }
  }
  else if (local_e9 == '\0') {
    iVar8 = *(int *)(DAT_00c71678 + 0x264f8) - param_1[0xca];
    if (param_1[0xb] == 100) {
      if (iVar8 == 3) {
        param_1[0x56] = param_1[0x56] | 2;
      }
      else if (iVar8 == 4) {
        uVar9 = RNG__Next();
        iVar8 = FUN_009dcc70(uVar9,0);
        param_1[0xc] = iVar8;
        FUN_006e21f0();
        uVar7 = param_1[0xc];
        if (DAT_00c71678 == 0) {
          if (-1 < (int)uVar7) goto LAB_006e4fc5;
        }
        else {
          if ((int)uVar7 < 0) {
            if (((int)uVar7 < 0) &&
               ((int)~uVar7 <
                *(int *)(DAT_00c71678 + 0x6775c) - *(int *)(DAT_00c71678 + 0x67758) >> 2)) {
              iVar8 = **(int **)(*(int *)(DAT_00c71678 + 0x67758) + ~uVar7 * 4);
            }
            else {
              iVar8 = 0;
            }
          }
          else {
LAB_006e4fc5:
            if (*(int *)(DAT_00c7169c + 0x2a408) - *(int *)(DAT_00c7169c + 0x2a404) >> 2 <=
                (int)uVar7) goto LAB_006e5401;
            iVar8 = *(int *)(*(int *)(DAT_00c7169c + 0x2a404) + uVar7 * 4);
          }
          if (iVar8 != 0) {
            param_1[0x149] = *(int *)(iVar8 + 0x74);
            if (-1 < *(int *)(iVar8 + 200)) {
              param_1[0x149] = *(int *)(iVar8 + 200);
            }
          }
        }
      }
      else if (4 < iVar8) goto LAB_006e5014;
    }
    else if (iVar8 < 6) {
      if (((iVar8 == 5) && (FUN_0040a780(), param_1[0x1f] != 0)) &&
         (FUN_00408e00(), param_1[0x1f] != 0)) {
        *(undefined1 *)(param_1 + 0x23) = 0;
      }
    }
    else if ((iVar8 < 10) || ((iVar8 < 0xf && (uVar7 = FUN_006eef60(), (uVar7 & 7) != 0)))) {
      if (((uint)param_1[0x56] >> 1 & 1) == 0) {
        uVar7 = FUN_006eef60();
        if (uVar7 % 6 == 0) {
          param_1[0x56] = param_1[0x56] | 2;
        }
        else {
          uVar7 = FUN_006eef60();
          if ((uVar7 & 7) == 0) {
            FUN_006eef60();
            FUN_0040a780();
            FUN_0040a720();
          }
        }
      }
      else {
        uVar7 = FUN_006eef60();
        if ((uVar7 & 1) == 0) {
          param_1[0x56] = param_1[0x56] & 0xfffffffd;
        }
      }
    }
    else {
      param_1[0x56] = param_1[0x56] & 0xfffffffd;
      param_1[0x5b] = param_1[0x5b] & 0xfffffeff;
      param_1[0x5a] = param_1[0x5a];
      puVar11 = (undefined4 *)FUN_00452bf0();
      local_14 = 5;
      if (0xf < (uint)puVar11[5]) {
        puVar11 = (undefined4 *)*puVar11;
      }
      cVar5 = FUN_0040a5d0(puVar11,1);
      if (cVar5 != '\0') {
        FUN_0040a1b0();
        *(undefined1 *)(param_1 + 0x23) = 1;
      }
      local_14 = 0xffffffff;
      FUN_0040d040();
      pfVar17 = (float *)FUN_0067f070();
      local_c4 = (float *)(*pfVar17 * DAT_00baa7e8);
      local_dc = (float *)(pfVar17[1] * DAT_00baa7e8);
      RNG__game_constructor(param_1[0xfb],3);
      uVar9 = RNG__Next();
      local_f4 = (int *)((float)local_c4 + (float)param_1[0xcf]);
      local_f0 = (float *)((float)local_dc + (float)param_1[0xd0]);
      piVar10 = (int *)FUN_00428b20(param_1[10],param_1[0xb],&local_f4,&DAT_00c7b640,param_1[0xf2],
                                    param_1[0xc],uVar9);
      (**(code **)(*piVar10 + 0xc))();
      param_1[0xcf] = (int)((float)param_1[0xcf] - (float)local_c4);
      param_1[0xd0] = (int)((float)param_1[0xd0] - (float)local_dc);
    }
  }
  else {
LAB_006e5014:
    param_1[0x56] = param_1[0x56] & 0xfffffffd;
    param_1[0x5a] = param_1[0x5a];
    param_1[0x5b] = param_1[0x5b] & 0xfffffeff;
  }
LAB_006e5401:
  if ((param_1[0xb] == 0x3a) && (param_1[0xc] != 0)) {
    local_48 = (float *)param_1[0x5a];
    uVar7 = param_1[0x5b];
    if (((uVar7 & 0x2000000) == 0) || (((uVar7 & 0x4000000) != 0 || (param_1[0xf0] != 0)))) {
      if ((param_1[0x153] < 1) && ((param_1[0x62] != 0 && ((uVar7 & 0x6000000) == 0)))) {
        iVar8 = FUN_00703950();
        fVar22 = (float)param_1[0xcf] - *(float *)(iVar8 + 0x33c);
        fVar24 = (float)param_1[0xd0] - *(float *)(iVar8 + 0x340);
        if (fVar24 * fVar24 + fVar22 * fVar22 < DAT_00baac34) {
          uVar9 = RNG__Next();
          piVar10 = (int *)FUN_00428b20(0x330,0,param_1 + 0xcf,&DAT_00c7b640,param_1,0,uVar9);
          piVar10[0xd6] = 0x40c00000;
          param_1[0x5b] = param_1[0x5b] | 0x2000000;
          param_1[0x5a] = param_1[0x5a];
          piVar10[0x5a] = piVar10[0x5a] & 0xfffffffb;
          piVar10[0x5b] = piVar10[0x5b];
          (**(code **)(*piVar10 + 0xc))();
          uVar27 = FUN_004238f0();
          (*(code *)((ulonglong)uVar27 >> 0x20))((int)uVar27,5,0xff,1,1);
          FUN_006a92e0();
        }
      }
    }
    else {
      *(undefined1 *)((int)param_1 + 0x171) = 1;
      cVar5 = FUN_006e6e40();
      if (cVar5 != '\0') {
        FUN_006ee750();
        iVar8 = *(int *)(*(int *)(DAT_00c71678 + 0x18300) + 8);
        if ((iVar8 == 0xb) || (iVar8 == 0x11)) {
          FUN_00833420();
        }
      }
    }
  }
  if ((param_1[0xb] == 10) && (param_1[0xc] == 0xc)) {
    if (param_1[0x1f] == 0) {
      local_bd = '\0';
LAB_006e55e8:
      fVar22 = (float)param_1[0xd8] * (float)param_1[0xd8] +
               (float)param_1[0xd9] * (float)param_1[0xd9];
      FUN_00435a50();
      if ((fVar22 <= DAT_00baa6fc) || (uVar7 = FUN_006eef60(), uVar7 % 3 != 0)) goto LAB_006e58be;
    }
    else {
      local_bd = FUN_0040add0();
      if (local_bd == '\0') goto LAB_006e55e8;
    }
    uVar9 = FUN_006eef60();
    piVar10 = (int *)FUN_00428b20(1000,7,param_1 + 0xcf,&DAT_00c7b640,0,0,uVar9);
    iVar8 = FUN_006eef60();
    pcVar1 = *(code **)(*piVar10 + 0x3c);
    fVar24 = (float)((double)iVar8 + (double)(&DAT_00bacb00)[-(iVar8 >> 0x1f)]) * DAT_00ba9ff4 *
             DAT_00baa280 + DAT_00baa198;
    fVar22 = fVar24 * DAT_00c3793c;
    piVar10[0x3a] = (int)(fVar24 * DAT_00c37940);
    piVar10[0x39] = (int)fVar22;
    FUN_00682ed0();
    local_94._0_1_ = s_333_fff_ff___00bac5a0[0];
    local_94._1_1_ = s_333_fff_ff___00bac5a0[1];
    local_94._2_1_ = s_333_fff_ff___00bac5a0[2];
    local_94._3_1_ = s_333_fff_ff___00bac5a0[3];
    iStack_90._0_1_ = s_333_fff_ff___00bac5a0[4];
    iStack_90._1_1_ = s_333_fff_ff___00bac5a0[5];
    iStack_90._2_1_ = s_333_fff_ff___00bac5a0[6];
    iStack_90._3_1_ = s_333_fff_ff___00bac5a0[7];
    iStack_8c._0_1_ = s_333_fff_ff___00bac5a0[8];
    iStack_8c._1_1_ = s_333_fff_ff___00bac5a0[9];
    iStack_8c._2_1_ = s_333_fff_ff___00bac5a0[10];
    iStack_8c._3_1_ = s_333_fff_ff___00bac5a0[0xb];
    iStack_88 = ram0x00bac5ac;
    (*pcVar1)(&local_94,0xffffffff,0xff,0,1);
    (**(code **)(*piVar10 + 0xc))();
    param_1 = local_f8;
    if (local_bd != '\0') {
      uVar7 = FUN_006eef60();
      param_1 = local_f8;
      for (iVar8 = uVar7 % 3 + 1; iVar8 != 0; iVar8 = iVar8 + -1) {
        iVar16 = FUN_006eef60();
        fVar22 = (float)((double)iVar16 + (double)(&DAT_00bacb00)[-(iVar16 >> 0x1f)]) * DAT_00ba9ff4
        ;
        local_d0 = (float *)(fVar22 + fVar22 + DAT_00baa454);
        iVar16 = FUN_006eef60();
        fVar22 = (float)((double)iVar16 + (double)(&DAT_00bacb00)[-(iVar16 >> 0x1f)]) * DAT_00ba9ff4
                 * DAT_00baa704;
        pfVar17 = (float *)(fVar22 + fVar22);
        local_c4 = pfVar17;
        FUN_0041d520();
        local_cc = pfVar17;
        iVar16 = FUN_006eef60();
        local_dc = (float *)((float)((double)iVar16 + (double)(&DAT_00bacb00)[-(iVar16 >> 0x1f)]) *
                             DAT_00ba9ff4 * DAT_00baa2d0 * (float)param_1[0xdc]);
        pfVar17 = local_c4;
        FUN_0041d540();
        local_44 = (float *)((float)pfVar17 * (float)local_dc + (float)param_1[0xcf]);
        local_40 = (float *)((float)local_cc * (float)local_dc + (float)param_1[0xd0]);
        iVar16 = FUN_006eef60();
        fVar22 = (float)((double)iVar16 + (double)(&DAT_00bacb00)[-(iVar16 >> 0x1f)]) * DAT_00ba9ff4
                 * DAT_00baa704;
        pfVar20 = (float *)(fVar22 + fVar22);
        local_c4 = pfVar20;
        FUN_0041d520();
        pfVar17 = local_c4;
        local_dc = pfVar20;
        FUN_0041d540();
        local_30 = CONCAT44((float)pfVar17 * (float)local_d0,(int)local_30);
        local_28 = (float)local_d0 * (float)local_dc * DAT_00baa2d0;
        uVar9 = FUN_006eef60();
        FUN_00428b20(1000,0x3f,&local_44,(int)&local_30 + 4,0,0,uVar9);
      }
    }
  }
LAB_006e58be:
  if ((((param_1[0xb] == 0x39) && (param_1[0xc] != 0)) && (param_1[0x1f] != 0)) &&
     (cVar5 = FUN_0040add0(), cVar5 != '\0')) {
    if (param_1[0xc] == 1) {
      cVar5 = FUN_006e6e40();
      if (cVar5 != '\0') {
        FUN_006ee750();
        iVar8 = *(int *)(*(int *)(DAT_00c71678 + 0x18300) + 8);
        if ((iVar8 == 0xb) || (iVar8 == 0x11)) {
          FUN_00833420();
        }
      }
    }
    else {
      param_1[0xc] = param_1[0xc] + -1;
    }
  }
  if (((param_1[0xb] == 100) && (*(int *)(DAT_00c71678 + 0x1830c) == 2)) &&
     ((param_1[0x14a] == 1 && ((0 < *(int *)(DAT_00c71678 + 0x68d6c) && (param_1[0x150] < 1)))))) {
    uVar9 = FUN_006eef60();
    local_28 = (float)param_1[0xd0] + DAT_00baa81c;
    local_30 = CONCAT44((float)param_1[0xcf] + DAT_00ba9fe4,(int)local_30);
    FUN_00428b20(1000,0xf,(int)&local_30 + 4,&DAT_00c7b640,0,0,uVar9);
    param_1[0x150] = 4;
  }
  if ((0 < param_1[0x150]) && (iVar8 = param_1[0x150] + -1, param_1[0x150] = iVar8, iVar8 == 0)) {
    (**(code **)(*param_1 + 0x28))();
  }
  if (0 < param_1[0x151]) {
    param_1[0x151] = param_1[0x151] + -1;
  }
  if (((0 < param_1[0x152]) && (iVar8 = param_1[0x152] + -1, param_1[0x152] = iVar8, iVar8 == 0)) &&
     (param_1[0xb] == 0x35)) {
    param_1[0xc] = 1;
    FUN_0040a380("Close",0);
    local_c4 = (float *)0x15;
    FUN_00956780();
    FUN_0092dc30(local_c4,0x3f800000,2,0,0x3f800000,0);
    param_1[0x151] = 0x1e;
    FUN_006e17c0();
  }
  iVar8 = *(int *)(DAT_00c71678 + 0x18300);
  if (*(int *)(iVar8 + 8) == 0x10) {
    local_c8 = (float)param_1[0xcf] + DAT_00ba9fe4;
    local_c4 = (float *)((float)param_1[0xde] * (float)param_1[0xdc] + DAT_00baa2d0 +
                        (float)param_1[0xd0]);
    iVar16 = FUN_007f0780(local_c8,local_c4);
    if (iVar16 != 4) {
      piVar10 = *(int **)(*(int *)(iVar8 + 4) + 0x10);
      if (((piVar10 == (int *)0x0) || (piVar10[2] != 0x10)) || (*piVar10 != 0x23)) {
        param_1[0xd9] = (int)((float)param_1[0xd9] + DAT_00baa3e0);
      }
      else {
        param_1[0xd9] = (int)((float)param_1[0xd9] + DAT_00baa280);
        param_1[0xdb] = (int)((float)param_1[0xdb] * DAT_00baa418);
      }
    }
    piVar10 = *(int **)(*(int *)(*(int *)(DAT_00c71678 + 0x18300) + 4) + 0x10);
    if (((piVar10 != (int *)0x0) && (piVar10[2] == 0x10)) &&
       ((*piVar10 == 0x23 &&
        (((2 < *(int *)(DAT_00c71678 + 0x264f8) - param_1[0xca] &&
          (DAT_00ba9fe4 < (float)param_1[0xd9])) &&
         (*(float *)(*(int *)(DAT_00c71678 + 0x18300) + 0x20) - DAT_00baa8d0 < (float)param_1[0xd0])
         ))))) {
      (**(code **)(*param_1 + 0x28))();
      uVar9 = FUN_006eef60();
      piVar10 = (int *)FUN_00428b20(1000,0x10,param_1 + 0xcf,&DAT_00c7b640,0,0x42,uVar9);
      (**(code **)(*piVar10 + 0xc))();
    }
  }
  cVar5 = FUN_00665c60();
  if ((cVar5 != '\0') &&
     (((iVar8 = param_1[0xb], iVar8 == 10 || (iVar8 == 0x1e)) ||
      ((((iVar8 == 0x28 || ((iVar8 == 0x14 || (iVar8 == 0x46)))) || (iVar8 == 0x5a)) ||
       (((iVar8 == 300 || (iVar8 == 0x15e)) || (cVar5 = FUN_006ee340(), cVar5 != '\0')))))))) {
    param_1[0xd8] = (int)DAT_00c7b640;
    param_1[0xd9] = (int)DAT_00c7b644;
    iVar8 = FUN_00703ab0(param_1 + 0xcf,1,0,0);
    if (iVar8 != 0) {
      fVar22 = (float)param_1[0xdb];
      fVar24 = *(float *)(iVar8 + 0x1660);
      if (fVar22 != DAT_00ba9fe4) {
        param_1[0xd9] =
             (int)(((float)param_1[0xe7] * (*(float *)(iVar8 + 0x1664) + *(float *)(iVar8 + 0x1664))
                   ) / fVar22 + (float)param_1[0xd9]);
        param_1[0xd8] =
             (int)(((float)param_1[0xe7] * (fVar24 + fVar24)) / fVar22 + (float)param_1[0xd8]);
      }
    }
  }
  cVar5 = FUN_00665c60();
  if ((cVar5 != '\0') || (cVar5 = FUN_00665c60(), cVar5 != '\0')) {
    iVar8 = DAT_00c71678;
    if (*(int *)(DAT_00c71678 + 0x264f8) - param_1[0xca] < 2) {
      local_cc = (float *)(((float)param_1[0xd0] - DAT_00baaa30) * DAT_00baa324 +
                          (DAT_00c78edc - DAT_00baaa7c) * DAT_00baa2d0);
      local_c4 = (float *)(DAT_00bf941c * DAT_00bf93e8);
      local_dc = (float *)((((float)param_1[0xcf] - DAT_00baa950) * DAT_00baa324 +
                           (DAT_00c78dc4 - DAT_00baab20) * DAT_00baa2d0) * (float)local_c4 +
                          DAT_00baa2d0);
      dVar28 = floor((double)(float)local_dc);
      local_d0 = (float *)((float)dVar28 / (float)local_c4);
      local_dc = (float *)((float)local_c4 * (float)local_cc + DAT_00baa2d0);
      dVar28 = floor((double)(float)local_dc);
      local_c4 = (float *)((float)dVar28 / (float)local_c4);
      local_cc = *(float **)(*(int *)(iVar8 + 0x18300) + 0x11fc);
      local_dc = *(float **)(*(int *)(iVar8 + 0x18300) + 0x1200);
      FUN_0041c770();
      local_14 = 6;
      pcVar1 = *(code **)(*local_f4 + 0x2c);
      FUN_00aefca0();
      uVar9 = FUN_00aefca0();
      (*pcVar1)(&local_50,uVar9);
      local_14 = 7;
      if (((local_f0 != (float *)0x0) &&
          (cVar5 = (**(code **)((int)*local_f0 + 0xc))(), cVar5 != '\0')) &&
         (DAT_00c71644 != (code *)0x0)) {
        (*DAT_00c71644)();
      }
      param_1 = local_f8;
      fVar22 = DAT_00baa3e0;
      local_14 = 0xffffffff;
      fVar24 = local_50 * DAT_00baa3e0;
      local_f8[0x159] = 0x3f800000;
      local_f8[0x156] = 0;
      local_f8[0x157] = 0;
      local_f8[0x158] = 0;
      local_f8[0x159] = 0x3f333333;
      local_f8[0x15e] = (int)fVar24;
      local_f8[0x15f] = (int)(local_4c * fVar22);
      local_f8[0x160] = (int)((float)local_48 * fVar22);
      FUN_004073d0();
    }
    iVar8 = DAT_00c71678;
    if ((uint)(*(int *)(DAT_00c71678 + 0x264f8) + param_1[8]) % 0x1e < 2) {
      local_cc = (float *)(((float)param_1[0xd0] - DAT_00baaa30) * DAT_00baa324 +
                          (DAT_00c78edc - DAT_00baaa7c) * DAT_00baa2d0);
      local_c4 = (float *)(DAT_00bf941c * DAT_00bf93e8);
      local_dc = (float *)((float)local_c4 *
                           (((float)param_1[0xcf] - DAT_00baa950) * DAT_00baa324 +
                           (DAT_00c78dc4 - DAT_00baab20) * DAT_00baa2d0) + DAT_00baa2d0);
      dVar28 = floor((double)(float)local_dc);
      local_f8 = (int *)((float)dVar28 / (float)local_c4);
      local_dc = (float *)((float)local_c4 * (float)local_cc + DAT_00baa2d0);
      dVar28 = floor((double)(float)local_dc);
      local_c4 = (float *)((float)dVar28 / (float)local_c4);
      local_cc = *(float **)(*(int *)(iVar8 + 0x18300) + 0x11fc);
      local_dc = *(float **)(*(int *)(iVar8 + 0x18300) + 0x1200);
      FUN_0041c770();
      local_14 = 8;
      (**(code **)(*local_d4 + 0x2c))
                (&local_50,(int)((float)local_f8 - (float)local_cc),
                 (int)((float)local_c4 - (float)local_dc));
      local_14 = 9;
      if (((local_d0 != (float *)0x0) &&
          (cVar5 = (**(code **)((int)*local_d0 + 0xc))(), cVar5 != '\0')) &&
         (DAT_00c71644 != (code *)0x0)) {
        (*DAT_00c71644)();
      }
      fVar24 = DAT_00baa3e0;
      fVar22 = DAT_00baa2d0;
      local_14 = 0xffffffff;
      fVar25 = (float)local_48 * DAT_00baa3e0;
      local_4c = local_4c * DAT_00baa3e0;
      param_1[0x159] =
           (int)((DAT_00baa354 - (float)param_1[0x159]) * DAT_00baa1f8 + (float)param_1[0x159]);
      param_1[0x160] = (int)((fVar25 - (float)param_1[0x160]) * fVar22 + (float)param_1[0x160]);
      param_1[0x15f] = (int)((local_4c - (float)param_1[0x15f]) * fVar22 + (float)param_1[0x15f]);
      param_1[0x15e] =
           (int)((local_50 * fVar24 - (float)param_1[0x15e]) * fVar22 + (float)param_1[0x15e]);
    }
    local_94 = param_1[0x3c];
    iStack_90 = param_1[0x3d];
    iStack_8c = param_1[0x3e];
    iStack_88 = param_1[0x3f];
    local_6c = param_1[0x46];
    local_84 = param_1[0x40];
    iStack_80 = param_1[0x41];
    iStack_7c = param_1[0x42];
    iStack_78 = param_1[0x43];
    local_74 = *(undefined8 *)(param_1 + 0x44);
    FUN_006832e0(local_124,&local_94,param_1 + 0x156,0x3dcccccd);
    iVar3 = _UNK_00bac0dc;
    iVar16 = _UNK_00bac0d8;
    iVar8 = _UNK_00bac0d4;
    if (param_1 + 0x3c != local_124) {
      param_1[0x3c] = _DAT_00bac0d0;
      param_1[0x3d] = iVar8;
      param_1[0x3e] = iVar16;
      param_1[0x3f] = iVar3;
      param_1[0x40] = local_114;
      param_1[0x41] = iStack_110;
      param_1[0x42] = iStack_10c;
      param_1[0x43] = iStack_108;
      *(undefined8 *)(param_1 + 0x44) = local_104;
      param_1[0x46] = local_fc;
    }
  }
  iVar8 = DAT_00c71678;
  uVar7 = param_1[0x150];
  if (((int)uVar7 < 1) || (param_1[0xb] == 100)) {
    cVar5 = FUN_00665c60();
    if (cVar5 != '\0') {
      iVar16 = param_1[0xca];
      uVar7 = *(int *)(iVar8 + 0x264f8) - iVar16;
      if (0x96 < (int)uVar7) {
        uVar7 = uVar7 & 0x80000001;
        if ((int)uVar7 < 0) {
          uVar7 = (uVar7 - 1 | 0xfffffffe) + 1;
        }
        if (uVar7 == 1) {
          FUN_00682ed0();
          local_74 = 0;
          local_94 = 0;
          iStack_90 = 0;
          iStack_8c = 0;
          iStack_88 = 0;
          local_6c = 0;
          (**(code **)(*param_1 + 0x3c))(&local_94,1,0xff,0,1);
          iVar16 = param_1[0xca];
        }
      }
      if (0xd2 < *(int *)(DAT_00c71678 + 0x264f8) - iVar16) {
LAB_006e42ba:
        (**(code **)(*param_1 + 0x28))();
        ExceptionList = local_1c;
        return;
      }
    }
  }
  else if ((int)uVar7 < 0x1e) {
    uVar7 = uVar7 & 0x80000001;
    if ((int)uVar7 < 0) {
      uVar7 = (uVar7 - 1 | 0xfffffffe) + 1;
    }
    if (uVar7 == 1) {
      FUN_00682ed0();
      local_48 = (float *)0x0;
      local_44 = (float *)0x0;
      local_68 = 0;
      uStack_64 = 0;
      uStack_60 = 0;
      uStack_5c = 0;
      local_40 = (float *)0x0;
      (**(code **)(*param_1 + 0x3c))(&local_68,1,0xff,0,1);
    }
  }
  if ((param_1[0xb] == 0x14) && (param_1[0xc] == 6)) {
    FUN_00452bf0();
    local_bd = FUN_0040cae0("Touched",7);
    FUN_0040d040();
    if (local_bd != '\0') {
      if ((param_1[0x1f] != 0) && (cVar5 = FUN_0040add0(), cVar5 != '\0')) {
        local_c4 = (float *)0xe7;
        FUN_00956780();
        FUN_0092dc30(local_c4,0x3f000000,2,0,0x3f800000,0);
      }
      if ((param_1[0x1f] == 0) || ((char)param_1[0x23] == '\0')) {
        FUN_0040a380(&DAT_00b1bc54,0);
      }
    }
  }
  if (0 < param_1[0x153]) {
    if ((param_1[0x1f] == 0) || ((char)param_1[0x23] == '\0')) {
LAB_006e6519:
      param_1[0x153] = param_1[0x153] + -1;
    }
    else {
      pbVar12 = (byte *)param_1[0x1f];
      if (0xf < *(uint *)(pbVar12 + 0x14)) {
        pbVar12 = *(byte **)pbVar12;
      }
      pcVar15 = "Appear";
      do {
        bVar6 = *pbVar12;
        bVar21 = bVar6 < (byte)*pcVar15;
        if (bVar6 != *pcVar15) {
LAB_006e64d7:
          uVar7 = -(uint)bVar21 | 1;
          goto LAB_006e64dc;
        }
        if (bVar6 == 0) break;
        bVar6 = pbVar12[1];
        bVar21 = bVar6 < (byte)pcVar15[1];
        if (bVar6 != pcVar15[1]) goto LAB_006e64d7;
        pbVar12 = pbVar12 + 2;
        pcVar15 = pcVar15 + 2;
      } while (bVar6 != 0);
      uVar7 = 0;
LAB_006e64dc:
      if (uVar7 != 0) {
        pbVar12 = (byte *)param_1[0x1f];
        if (0xf < *(uint *)(pbVar12 + 0x14)) {
          pbVar12 = *(byte **)pbVar12;
        }
        pcVar15 = "AppearFast";
        do {
          bVar6 = *pbVar12;
          bVar21 = bVar6 < (byte)*pcVar15;
          if (bVar6 != *pcVar15) {
LAB_006e6510:
            uVar7 = -(uint)bVar21 | 1;
            goto LAB_006e6515;
          }
          if (bVar6 == 0) break;
          bVar6 = pbVar12[1];
          bVar21 = bVar6 < (byte)pcVar15[1];
          if (bVar6 != pcVar15[1]) goto LAB_006e6510;
          pbVar12 = pbVar12 + 2;
          pcVar15 = pcVar15 + 2;
        } while (bVar6 != 0);
        uVar7 = 0;
LAB_006e6515:
        if (uVar7 != 0) goto LAB_006e6519;
      }
    }
  }
  if (param_1[0xb] == 0x154) {
    local_dc = (float *)param_1[0xf1];
    if ((local_dc == (float *)0x0) || (local_dc[10] != 1.4013e-45)) {
      local_dc = (float *)PlayerManager__get_player_417870();
    }
    if (param_1[0x161] == 1) {
      FUN_0040a380(&DAT_00b1d644,0);
      uVar7 = 0;
      if (*(int *)(DAT_00c71678 + 0x1baac) - *(int *)(DAT_00c71678 + 0x1baa8) >> 2 != 0) {
        do {
          iVar16 = FUN_009b92c0();
          iVar8 = DAT_00c71678;
          uVar7 = uVar7 + 1;
          piVar10 = (int *)(DAT_00c71678 + 0x1baa8);
          *(float *)(iVar16 + 0x360) = DAT_00c7b640;
          *(float *)(iVar16 + 0x364) = DAT_00c7b644;
          *(undefined1 *)(iVar16 + 0x410) = 0;
        } while (uVar7 < (uint)(*(int *)(iVar8 + 0x1baac) - *piVar10 >> 2));
      }
      param_1[0x5b] = param_1[0x5b] | 0x1000;
      param_1[0x161] = param_1[0x161] + 1;
      param_1[0x5a] = param_1[0x5a];
      param_1[0x62] = 0;
      local_dc[0x6c7] = DAT_00c7b640;
      local_dc[0x6c8] = DAT_00c7b644;
      FUN_006fdc10(0,4,local_dc);
      iVar8 = FUN_006f9d20();
      if ((((iVar8 != 3) && (iVar8 != 4)) && (iVar8 != 5)) && ((iVar8 != 9 && (iVar8 != 0xc)))) {
        FUN_009568e0(0x433,2,0,0x3f800000);
      }
    }
    else if (param_1[0x161] == 2) {
      iVar8 = FUN_0040a780();
      if ((iVar8 == 6) &&
         (((iVar8 = FUN_006f9d20(), iVar8 == 3 || (iVar8 == 4)) ||
          ((iVar8 == 5 || ((iVar8 == 9 || (iVar8 == 0xc)))))))) {
        FUN_006f9770();
        ExceptionList = local_1c;
        return;
      }
      if ((param_1[0x1f] == 0) || ((char)param_1[0x23] == '\0')) {
        param_1[0x161] = param_1[0x161] + 1;
        local_c4 = (float *)0x41c;
        FUN_00956780();
        FUN_0092dc30(local_c4,0x3f800000,2,0,0x3f800000,0);
        pfVar17 = local_dc;
        FUN_007abe20();
        fVar22 = (float)param_1[0xd0] + DAT_00baa87c;
        pfVar17[0x6c7] = (float)param_1[0xcf] + DAT_00ba9fe4;
        pfVar17[0x6c8] = fVar22;
      }
    }
  }
  if (param_1[0xb] != 0x172) goto LAB_006e686a;
  iVar8 = param_1[0xf1];
  if ((iVar8 == 0) || (*(int *)(iVar8 + 0x28) != 1)) {
    param_1[0x161] = 0;
    goto LAB_006e686a;
  }
  if (param_1[0x161] == 1) {
    *(undefined4 *)(iVar8 + 0x188) = 0;
    *(undefined1 *)(iVar8 + 0x410) = 0;
    FUN_007ab130(param_1 + 0x12,1,"Pickup");
    param_1[0x161] = param_1[0x161] + 1;
    *(undefined1 *)((int)param_1 + 0x171) = 0;
    goto LAB_006e686a;
  }
  if (param_1[0x161] != 2) goto LAB_006e686a;
  if (*(char *)(iVar8 + 0x139a) == '\0') {
LAB_006e67da:
    cVar5 = FUN_007bf490();
    if (cVar5 != '\0') goto LAB_006e686a;
  }
  else {
    if (*(int *)(iVar8 + 0x450) == 0) {
      local_c4 = (float *)0x0;
    }
    else {
      local_c4 = *(float **)(*(int *)(iVar8 + 0x450) + 0x30);
    }
    puVar14 = (undefined1 *)FUN_0040a780();
    if (puVar14 != (undefined1 *)((int)local_c4 + -1)) goto LAB_006e67da;
  }
  iVar16 = DAT_00c71678;
  *(undefined4 *)(iVar8 + 0x188) = 4;
  if (((*(int *)(iVar16 + 0x26630) == 0) || (iVar8 = FUN_006f9d20(), iVar8 == 0xff)) || (iVar8 == 0)
     ) {
    FUN_00704f20();
  }
  else {
    FUN_006f9770();
  }
LAB_006e686a:
  if ((((param_1[0xb] == 0x36) && (param_1[0xc] != 0)) &&
      ((param_1[0x153] < 1 && ((param_1[0x62] != 0 && (cVar5 = FUN_0044bfb0(), cVar5 == '\0'))))))
     && (iVar8 = FUN_00703950(), fVar24 = (float)param_1[0xcf] - *(float *)(iVar8 + 0x33c),
        fVar22 = (float)param_1[0xd0] - *(float *)(iVar8 + 0x340),
        fVar22 * fVar22 + fVar24 * fVar24 < DAT_00baabf0)) {
    FUN_006e30a0(param_1[10],0x34,param_1[0xc],0,0,0);
    FUN_0040a380("Appear",0);
    if (param_1[0x1f] != 0) {
      FUN_00408e00();
    }
    param_1[0x62] = 4;
    FUN_009568e0(0xcd,2,0,0x3f800000);
  }
  FUN_00862fe0();
  ExceptionList = local_1c;
  return;
}
