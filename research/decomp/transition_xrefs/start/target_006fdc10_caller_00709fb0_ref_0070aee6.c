/* Static decompilation only; PE entry point was not executed. */
/* Target: 006fdc10 */
/* Reference: 0070aee6 */
/* Caller: FUN_00709fb0 @ 00709fb0 */


void __thiscall
FUN_00709fb0(int param_1,int *param_2,int param_3,float param_4,float param_5,float param_6)

{
  code *pcVar1;
  void **ppvVar2;
  char cVar3;
  uint uVar4;
  int iVar5;
  float *pfVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  int *piVar10;
  int iVar11;
  int iVar12;
  uint uVar13;
  int extraout_EDX;
  uint *puVar14;
  uint uVar15;
  float10 fVar16;
  float fVar17;
  float fVar18;
  float fVar19;
  float fVar20;
  float in_XMM2_Da;
  undefined4 local_68;
  undefined4 local_64;
  undefined4 local_40;
  undefined8 local_3c;
  undefined4 local_34;
  undefined1 local_30 [4];
  int local_2c;
  uint local_28;
  undefined8 local_24;
  uint local_1c;
  float local_18;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;

  local_8 = 0xffffffff;
  puStack_c = &LAB_00afc5bd;
  local_10 = ExceptionList;
  uVar4 = DAT_00bf93b4 ^ (uint)&stack0xfffffffc;
  if (((param_6._0_1_ == '\0') &&
      ((((iVar5 = param_2[0x61], iVar5 == 0 || (iVar5 == 3)) || (iVar5 == 1)) || (iVar5 == 2)))) ||
     (((uVar15 = (uint)param_4 & 0x80, uVar15 != 0 && ((param_2[0x5a] & 0x80000U) != 0)) ||
      ((iVar5 = param_2[10], iVar5 == 0x362 || (iVar5 == 0x322)))))) {
    return;
  }
  local_1c = (uint)param_4 & 2;
  ppvVar2 = &local_10;
  local_2c = param_1;
  local_18 = in_XMM2_Da;
  if (local_1c != 0) {
    if (iVar5 == 0x36) {
      return;
    }
    if (iVar5 == 0x1c) {
      if (param_2[0xb] == 2) {
        return;
      }
    }
    else if (iVar5 == 1) {
      ExceptionList = &local_10;
      cVar3 = FUN_009305f0(0x53);
      if (cVar3 != '\0') {
        ExceptionList = local_10;
        return;
      }
      iVar5 = param_2[10];
      ppvVar2 = ExceptionList;
    }
  }
  ExceptionList = ppvVar2;
  uVar13 = (uint)param_4 & 0x200;
  if (((uVar13 != 0) && (iVar5 == 0x1c)) && (param_2[0xb] == 2)) {
    ExceptionList = local_10;
    return;
  }
  if (((uVar15 != 0) && (iVar5 == 1)) && (param_6._0_1_ == '\0')) {
    cVar3 = FUN_00771550(0xe,0);
    if (cVar3 != '\0') {
      ExceptionList = local_10;
      return;
    }
    cVar3 = FUN_007706e0(0x23b,0);
    if (cVar3 != '\0') {
      ExceptionList = local_10;
      return;
    }
  }
  if (((uVar13 != 0) && (param_2[10] == 3)) && (param_2[0xb] == 0xc9)) {
    ExceptionList = local_10;
    return;
  }
  if (param_2[10] == 3) {
    if (param_2[0xb] == 0xce) {
      ExceptionList = local_10;
      return;
    }
    if (param_2[0xb] == 0xed) {
      ExceptionList = local_10;
      return;
    }
    if (param_2[0xb] == 0xee) {
      ExceptionList = local_10;
      return;
    }
  }
  FUN_00435c70(uVar4);
  local_64 = *(undefined4 *)(param_1 + 4);
  local_68 = 0;
  if ((extraout_EDX == 1) ||
     ((extraout_EDX == 3 && ((param_2[0xb] == 0x3e || (param_2[0xb] == 0x43)))))) {
    if (DAT_00c71678[0x9985] < 2) {
      local_18 = (float)param_3;
      FUN_006a9140();
      iVar5 = PlayerManager__condition_7cb6e0(0xe);
      if (((1 < iVar5) && (*(int *)(DAT_00c71678[0x60c0] + 8) == 0xd)) &&
         (*(int *)(param_1 + 4) == 8)) {
        local_18 = local_18 * DAT_00baa2d0;
      }
    }
    if ((param_2[10] == 1) && (uVar15 != 0)) {
      FUN_007b98c0(0x3ef0f0f1,0,0,0x3f800000,0,1);
    }
  }
  if ((char)param_2[0xec] != '\0') {
    ExceptionList = local_10;
    return;
  }
  cVar3 = (**(code **)(*param_2 + 0x20))(local_18,param_4,param_5,&local_68,0x1e);
  if (cVar3 == '\0') {
    ExceptionList = local_10;
    return;
  }
  if (local_1c != 0) {
    param_6 = (float)param_2[0xe0] * DAT_00baa0d0 + DAT_00baa2d0;
    FUN_009568e0(0x2b,2,0,0x3f800000);
  }
  pfVar6 = (float *)FUN_00709df0(&param_4);
  param_4 = (float)param_2[0xcf] - *pfVar6;
  param_5 = (float)param_2[0xd0] - pfVar6[1];
  pfVar6 = (float *)FUN_00a10030((int)&local_24 + 4);
  fVar18 = pfVar6[1] * DAT_00baa75c;
  param_2[0xd8] = (int)(*pfVar6 * DAT_00baa75c + (float)param_2[0xd8]);
  param_2[0xd9] = (int)(fVar18 + (float)param_2[0xd9]);
  if (*(int *)(param_1 + 4) != 8) {
    if (*(int *)(param_1 + 4) != 0x1c) {
      ExceptionList = local_10;
      return;
    }
    if (param_2[10] != 1) {
      if (param_2[10] != 3) {
        ExceptionList = local_10;
        return;
      }
      if (param_2[0xb] != 0x3e) {
        ExceptionList = local_10;
        return;
      }
    }
    if (uVar15 == 0) {
      ExceptionList = local_10;
      return;
    }
    *(int *)(param_1 + 0x18) = *(int *)(param_1 + 0x18) + 1;
    local_40 = *(undefined4 *)(param_1 + 0x14);
    local_3c = DAT_00b1f66c;
    local_34 = DAT_00b1f674;
    if (((*(int *)(param_1 + 0x18) < 2) && (iVar5 = RNG__RandomInt(2), iVar5 != 0)) &&
       (iVar5 = FUN_009bea80(0x38), iVar5 < 3)) {
      ExceptionList = local_10;
      return;
    }
    if (*(int *)(param_1 + 4) != 0x1c) {
      ExceptionList = local_10;
      return;
    }
    iVar11 = 0;
    fVar18 = (float)(*(int *)(param_1 + 0x24) % *(int *)(DAT_00c71678[0x60c0] + 0xc)) * DAT_00baa904
             + DAT_00baa904;
    fVar19 = (float)(*(int *)(param_1 + 0x24) / *(int *)(DAT_00c71678[0x60c0] + 0xc)) * DAT_00baa904
             + DAT_00baaa00;
    param_6 = DAT_00baaccc;
    FUN_0041af60(&local_28,5,100,0xffffffff,0,0);
    iVar5 = (int)local_24;
    uVar4 = 0;
    local_8 = 1;
    if (local_1c != 0) {
      do {
        iVar12 = __RTDynamicCast(*(undefined4 *)(iVar5 + uVar4 * 4),0,
                                 &IsaacRepentancePlus::Entity::RTTI_Type_Descriptor,
                                 &IsaacRepentancePlus::Entity_Pickup::RTTI_Type_Descriptor,0);
        if (((iVar12 != 0) && (*(int *)(iVar12 + 0x534) == -10)) &&
           (fVar17 = *(float *)(iVar12 + 0x33c) - fVar18,
           fVar20 = *(float *)(iVar12 + 0x340) - fVar19, fVar17 = fVar20 * fVar20 + fVar17 * fVar17,
           fVar17 < param_6)) {
          iVar11 = iVar12;
          param_6 = fVar17;
        }
        uVar4 = uVar4 + 1;
      } while (uVar4 < local_1c);
      if (iVar11 != 0) {
        FUN_006e2570(0);
        *(undefined1 *)(iVar11 + 0x538) = 0;
        if (*(int *)(iVar11 + 0x2c) == 100) {
          *(undefined4 *)(iVar11 + 0x584) = 1;
        }
      }
    }
    FUN_0071eb30(0);
    if ((char)local_28 != '\0') {
      ExceptionList = local_10;
      return;
    }
    if (DAT_00c7de78 == 0) {
      puVar14 = &DAT_00c7f618;
    }
    else {
      puVar14 = (uint *)(DAT_00c7de78 + 0x30);
    }
    if ((int)local_24 == 0) {
      ExceptionList = local_10;
      return;
    }
    uVar15 = *(uint *)((int)local_24 + -4);
    uVar4 = *puVar14;
    *puVar14 = *puVar14 - uVar15;
    puVar14[1] = puVar14[1] - (uint)(uVar4 < uVar15);
    free((uint *)((int)local_24 + -4));
    ExceptionList = local_10;
    return;
  }
  if (param_2[10] != 1) {
    if (param_2[10] != 3) {
      ExceptionList = local_10;
      return;
    }
    if (param_2[0xb] != 0x3e) {
      ExceptionList = local_10;
      return;
    }
  }
  if (uVar15 == 0) {
    ExceptionList = local_10;
    return;
  }
  if ((*(int *)(DAT_00c71678[0x60c0] + 8) != 0xd) && (*(uint *)(param_1 + 8) < 100)) {
    ExceptionList = local_10;
    return;
  }
  if ((*(uint *)(*(int *)(DAT_00c71678[0x60c0] + 4) + 0x44) >> 2 & 1) != 0) {
    ExceptionList = local_10;
    return;
  }
  iVar5 = FUN_006a89d0();
  if ((iVar5 == 0) || (*(int *)(iVar5 + 0x28) != 1)) {
    iVar5 = 0;
    iVar11 = 0;
  }
  else if ((*(int *)(iVar5 + 0x13c0) != 0x28) ||
          (iVar11 = *(int *)(iVar5 + 0x1e68), *(int *)(iVar5 + 0x1e68) == 0)) {
    iVar11 = iVar5;
  }
  local_28 = RNG__Next();
  local_24 = DAT_00b1f4e0;
  iVar12 = *(int *)(param_1 + 0x18);
  local_1c = DAT_00b1f4e8;
  *(int *)(param_1 + 0x18) = iVar12 + 1;
  if (99 < *(uint *)(param_1 + 8)) {
    fVar16 = (float10)RNG__RandomFloat();
    param_6 = (float)fVar16;
    if (param_6 < DAT_00baa154) {
      iVar5 = 6;
      uVar4 = local_28;
      do {
        if (uVar4 == 0) {
          Isaac__log(0x10,"RNG Seed is zero!\n");
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        uVar4 = uVar4 >> ((byte)local_24 & 0x1f) ^ uVar4;
        uVar4 = uVar4 << ((byte)((ulonglong)local_24 >> 0x20) & 0x1f) ^ uVar4;
        uVar4 = uVar4 >> ((byte)local_1c & 0x1f) ^ uVar4;
        param_4 = (float)(*(int *)(param_1 + 0x24) % *(int *)(DAT_00c71678[0x60c0] + 0xc)) *
                  DAT_00baa904 + DAT_00baa904;
        param_5 = (float)(*(int *)(param_1 + 0x24) / *(int *)(DAT_00c71678[0x60c0] + 0xc)) *
                  DAT_00baa904 + DAT_00baaa00;
        uVar7 = FUN_00813520(local_30,&param_4,0,0,0,0);
        FUN_00428b20(5,0x14,uVar7,&DAT_00c7b640,0,1,uVar4);
        iVar5 = iVar5 + -1;
      } while (iVar5 != 0);
      *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
      ExceptionList = local_10;
      return;
    }
    if (DAT_00baa2c4 <= param_6) {
      if (param_6 < DAT_00baa2f4) {
        iVar5 = 2;
        uVar4 = local_28;
        do {
          if (uVar4 == 0) {
            Isaac__log(0x10,"RNG Seed is zero!\n");
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
          uVar4 = uVar4 >> ((byte)local_24 & 0x1f) ^ uVar4;
          uVar4 = uVar4 << ((byte)((ulonglong)local_24 >> 0x20) & 0x1f) ^ uVar4;
          uVar4 = uVar4 >> ((byte)local_1c & 0x1f) ^ uVar4;
          param_4 = (float)(*(int *)(param_1 + 0x24) % *(int *)(DAT_00c71678[0x60c0] + 0xc)) *
                    DAT_00baa904 + DAT_00baa904;
          param_5 = (float)(*(int *)(param_1 + 0x24) / *(int *)(DAT_00c71678[0x60c0] + 0xc)) *
                    DAT_00baa904 + DAT_00baaa00;
          uVar7 = FUN_00813520(local_30,&param_4,0,0,0,0);
          FUN_00428b20(5,10,uVar7,&DAT_00c7b640,0,6,uVar4);
          iVar5 = iVar5 + -1;
        } while (iVar5 != 0);
        *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
        ExceptionList = local_10;
        return;
      }
      if (param_6 < DAT_00baa31c) {
        uVar7 = RNG__Next();
        uVar8 = FUN_00709df0(&param_4);
        uVar9 = FUN_00813520(local_30,uVar8,0,0,0,0);
        uVar8 = 0;
        goto LAB_0070ab5f;
      }
      if ((param_6 < DAT_00baa324) && (iVar11 != 0)) {
        FUN_0075e320(8,3);
        *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
        ExceptionList = local_10;
        return;
      }
    }
    else if (iVar11 != 0) {
      FUN_009302e0(0x2b4,0,1);
      *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
      ExceptionList = local_10;
      return;
    }
    goto LAB_0070af38;
  }
  switch(iVar12) {
  case 0:
  case 1:
    if (((DAT_00c71678[0x60e7] & 0x10000U) != 0) &&
       (iVar5 = PlayerManager__get_player_417870(0), *(int *)(iVar5 + 0x1364) < 1)) {
      RNG__Next();
      uVar7 = RNG__Next();
      param_4 = 320.0;
      param_5 = 340.0;
      uVar8 = FUN_00813520(local_30,&param_4,0,0,0,0);
      FUN_00428b20(5,0x28,uVar8,&DAT_00c7b640,0,1,uVar7);
      *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
      ExceptionList = local_10;
      return;
    }
    iVar5 = RNG__RandomInt(2);
    if (iVar5 == 0) {
      uVar7 = RNG__Next();
      param_4 = 320.0;
      param_5 = 340.0;
      uVar8 = FUN_00813520(local_30,&param_4,0,0,0,0);
      FUN_00428b20(5,0x14,uVar8,&DAT_00c7b640,0,1,uVar7);
      *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
      ExceptionList = local_10;
      return;
    }
    break;
  case 2:
    iVar5 = RNG__RandomInt(2);
    if (iVar5 == 0) {
      fVar18 = (float)DAT_00c71678[0x60bd] + DAT_00baa154;
      goto LAB_0070a7f1;
    }
    break;
  case 3:
    iVar5 = RNG__RandomInt(2);
    if (iVar5 == 0) goto LAB_0070a846;
    break;
  case 4:
    iVar5 = RNG__RandomInt(2);
    if (iVar5 != 0) {
      iVar5 = 3;
      uVar4 = local_28;
      do {
        if (uVar4 == 0) {
          Isaac__log(0x10,"RNG Seed is zero!\n");
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        uVar4 = uVar4 >> ((byte)local_24 & 0x1f) ^ uVar4;
        param_4 = 320.0;
        uVar4 = uVar4 << ((byte)((ulonglong)local_24 >> 0x20) & 0x1f) ^ uVar4;
        param_5 = 340.0;
        uVar4 = uVar4 >> ((byte)local_1c & 0x1f) ^ uVar4;
        uVar7 = FUN_00813520(local_30,&param_4,0,0,0,0);
        FUN_00428b20(5,0x14,uVar7,&DAT_00c7b640,0,1,uVar4);
        iVar5 = iVar5 + -1;
      } while (iVar5 != 0);
      *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
      ExceptionList = local_10;
      return;
    }
    fVar18 = (float)DAT_00c71678[0x60bd] + DAT_00baa2d0;
LAB_0070a7f1:
    iVar5 = DAT_00c7169c + 0x4a920;
    DAT_00c71678[0x60bd] = (int)fVar18;
    uVar7 = FUN_009586f0(iVar5,"#YOU_FEEL_BLESSED");
    FUN_009a36d0(uVar7);
    *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
    ExceptionList = local_10;
    return;
  case 5:
    iVar11 = RNG__RandomInt(3);
    if (iVar11 == 0) {
      FUN_007499a0(1,0);
      DAT_00c71678[0x60c6] = -1;
      FUN_007499a0(0,0);
      FUN_006fd7c0(0xffffffff,0xffffffff,3,iVar5,0xffffffff);
      *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
      ExceptionList = local_10;
      return;
    }
LAB_0070a846:
    uVar7 = RNG__Next();
    param_4 = 320.0;
    param_5 = 340.0;
    uVar8 = FUN_00813520(local_30,&param_4,0,0,0,0);
    FUN_00428b20(5,0x32,uVar8,&DAT_00c7b640,0,0,uVar7);
    *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
    ExceptionList = local_10;
    return;
  case 6:
    iVar5 = RNG__RandomInt(3);
    if (iVar5 == 0) {
      uVar7 = RNG__Next();
      uVar8 = RNG__Next();
      uVar8 = FUN_00733610(4,uVar8,0,0,0);
      param_4 = 320.0;
      param_5 = 340.0;
      uVar9 = FUN_00813520(local_30,&param_4,0,0,0,0);
    }
    else {
      if ((((iVar5 != 2) || (DAT_00c71678[0x995a] < 1)) ||
          (cVar3 = FUN_00732d00(0x2a1,0), cVar3 == '\0')) || (6 < *DAT_00c71678)) {
        uVar7 = RNG__Next();
        param_4 = 320.0;
        param_5 = 340.0;
        uVar8 = FUN_00813520(local_30,&param_4,0,0,0,0);
        FUN_00428b20(5,10,uVar8,&DAT_00c7b640,0,3,uVar7);
        *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
        ExceptionList = local_10;
        return;
      }
      uVar7 = RNG__Next();
      param_4 = 320.0;
      param_5 = 340.0;
      uVar9 = FUN_00813520(local_30,&param_4,0,0,0,0);
      uVar8 = 0x2a1;
    }
LAB_0070ab5f:
    FUN_00428b20(5,100,uVar9,&DAT_00c7b640,0,uVar8,uVar7);
    *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
    ExceptionList = local_10;
    return;
  case 7:
    *(undefined4 *)(DAT_00c71678[0x60c0] + 0x7230) = 0x23;
    *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
    ExceptionList = local_10;
    return;
  case 8:
    uVar7 = RNG__Next();
    param_4 = 320.0;
    param_5 = 340.0;
    uVar8 = FUN_00813520(local_30,&param_4,0,0,0,0);
    uVar9 = 0x10f;
    goto LAB_0070ac10;
  case 9:
    iVar5 = RNG__RandomInt(2);
    if (iVar5 != 0) {
      iVar5 = 0x1e;
      uVar4 = local_28;
      do {
        if (uVar4 == 0) {
          Isaac__log(0x10,"RNG Seed is zero!\n");
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        uVar4 = uVar4 >> ((byte)local_24 & 0x1f) ^ uVar4;
        param_4 = 320.0;
        uVar4 = uVar4 << ((byte)((ulonglong)local_24 >> 0x20) & 0x1f) ^ uVar4;
        param_5 = 340.0;
        uVar4 = uVar4 >> ((byte)local_1c & 0x1f) ^ uVar4;
        uVar7 = FUN_00813520(local_30,&param_4,0,0,0,0);
        FUN_00428b20(5,0x14,uVar7,&DAT_00c7b640,0,1,uVar4);
        iVar5 = iVar5 + -1;
      } while (iVar5 != 0);
      *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
      ExceptionList = local_10;
      return;
    }
    iVar5 = 7;
    uVar4 = local_28;
    do {
      if (uVar4 == 0) {
        Isaac__log(0x10,"RNG Seed is zero!\n");
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      uVar4 = uVar4 >> ((byte)local_24 & 0x1f) ^ uVar4;
      param_4 = 320.0;
      uVar4 = uVar4 << ((byte)((ulonglong)local_24 >> 0x20) & 0x1f) ^ uVar4;
      param_5 = 340.0;
      uVar4 = uVar4 >> ((byte)local_1c & 0x1f) ^ uVar4;
      uVar7 = FUN_00813520(local_30,&param_4,0,0,0,0);
      FUN_00428b20(5,10,uVar7,&DAT_00c7b640,0,3,uVar4);
      iVar5 = iVar5 + -1;
    } while (iVar5 != 0);
    *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
    ExceptionList = local_10;
    return;
  case 10:
    uVar7 = RNG__Next();
    param_4 = 320.0;
    param_5 = 340.0;
    uVar8 = FUN_00813520(local_30,&param_4,0,0,0,0);
    uVar9 = 0x110;
LAB_0070ac10:
    piVar10 = (int *)FUN_00428b20(uVar9,0,uVar8,&DAT_00c7b640,0,0,uVar7);
    (**(code **)(*piVar10 + 0xc))();
    *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
    ExceptionList = local_10;
    return;
  default:
    iVar11 = RNG__RandomInt(2);
    piVar10 = DAT_00c71678;
    if (((iVar11 == 0) && (DAT_00c71678[0x9a72] != 2)) && (DAT_00c71678[0x9a72] != 3)) {
      iVar12 = FUN_00706940();
      iVar11 = 0xc;
      if ((*(int *)(iVar12 + 0x40) != 0xc) &&
         (((piVar10[0x9961] != 0 || (piVar10[0x998c] != 0)) ||
          ((*(char *)(DAT_00c7169c + 0x18c) == '\0' &&
           ((*(int *)(DAT_00c7169c + 8) != 2 || (*(char *)((int)piVar10 + 0x26589) == '\0')))))))) {
        iVar11 = 0xb;
      }
      if (*(char *)(iVar12 + 0x7f) != '\0') {
        if (*(int *)(iVar12 + 0x80) == 1) break;
        if (*(int *)(iVar12 + 0x40) != 0) {
          iVar11 = *(int *)(iVar12 + 0x40);
        }
        if (*(int *)(iVar12 + 0x80) == 3) break;
      }
      if (10 < iVar11) {
        if ((*piVar10 == 0xb) && (piVar10[1] == 0)) {
          piVar10[0x60c6] = -1;
          FUN_006fd7c0(piVar10[0x60b4],0xffffffff,3,iVar5,0);
          *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
          ExceptionList = local_10;
          return;
        }
        FUN_006fdc10(0,2,0);
        FUN_007abe20("TeleportUp");
        param_6 = 3.01279e-43;
        FUN_00956780();
        FUN_0092dc30(param_6,0x3f800000,2,0,0x3f800000,0);
      }
    }
  }
LAB_0070af38:
  *(undefined4 *)(param_1 + 0x20) = *(undefined4 *)(param_1 + 0x2c);
  ExceptionList = local_10;
  return;
}
