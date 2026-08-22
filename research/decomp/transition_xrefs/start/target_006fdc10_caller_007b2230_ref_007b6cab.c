/* Static decompilation only; PE entry point was not executed. */
/* Target: 006fdc10 */
/* Reference: 007b6cab */
/* Caller: FUN_007b2230 @ 007b2230 */


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */
/* WARNING: Type propagation algorithm not settling */

void __thiscall FUN_007b2230(int *param_1,int param_2,uint param_3)

{
  bool bVar1;
  char cVar2;
  byte bVar3;
  uint uVar4;
  int *piVar5;
  code **ppcVar6;
  undefined4 uVar7;
  uint uVar8;
  char *pcVar9;
  int iVar10;
  undefined4 uVar11;
  undefined4 uVar12;
  undefined4 *puVar13;
  int iVar14;
  char *pcVar15;
  undefined1 *puVar16;
  uint uVar17;
  char *pcVar18;
  int *piVar19;
  code *pcVar20;
  int *piVar21;
  float10 fVar22;
  int *in_XMM0_Da;
  float fVar23;
  TypeDescriptor *pTVar24;
  TypeDescriptor *pTVar25;
  undefined4 uVar26;
  undefined1 local_488 [8];
  undefined1 local_480 [8];
  undefined4 local_478;
  undefined1 local_470 [8];
  undefined4 local_468;
  undefined1 local_460 [8];
  int local_458;
  undefined1 local_450 [8];
  int local_448;
  undefined1 local_440 [8];
  undefined1 local_438 [16];
  undefined1 local_428 [16];
  undefined1 local_418 [16];
  int local_408;
  undefined4 local_404;
  undefined4 local_400;
  undefined4 local_3fc;
  int local_3f8;
  undefined4 local_3f4;
  undefined4 local_3f0;
  undefined4 local_3ec;
  int local_3e8;
  undefined4 local_3e4;
  undefined4 local_3e0;
  undefined4 local_3dc;
  int local_3d8;
  undefined4 local_3d4;
  undefined4 local_3d0;
  undefined4 local_3cc;
  undefined1 local_3c8 [16];
  undefined1 local_3b8 [8];
  undefined1 local_3b0 [16];
  undefined1 local_3a0 [8];
  undefined1 local_398 [8];
  undefined1 local_390 [8];
  undefined4 local_388;
  undefined1 local_380 [8];
  undefined4 local_378;
  undefined1 local_374 [8];
  int local_36c;
  undefined1 local_368 [8];
  undefined1 local_360 [8];
  undefined1 local_358 [20];
  undefined1 local_344 [8];
  int local_33c;
  int local_338;
  undefined1 local_330 [20];
  undefined1 local_31c [8];
  undefined1 local_314 [4];
  undefined4 local_310;
  undefined4 local_30c;
  undefined1 local_308 [8];
  undefined1 local_300 [8];
  undefined4 local_2f8;
  undefined4 local_2f4;
  undefined1 local_2f0 [4];
  int *local_2ec;
  undefined4 local_2e8;
  undefined4 local_2e4;
  byte local_2de;
  byte local_2dd;
  undefined1 local_2dc [4];
  code *local_2d8;
  undefined4 local_2d4;
  undefined4 local_2d0;
  undefined4 local_2cc;
  int *local_2c8;
  undefined8 local_2c4;
  int *local_2bc [3];
  int *local_2b0;
  undefined4 local_2ac;
  undefined4 local_2a8;
  undefined1 local_2a2;
  byte local_2a1;
  int local_2a0;
  int *local_29c;
  undefined4 local_298;
  int local_294;
  undefined1 local_254 [12];
  undefined4 local_248;
  undefined4 uStack_244;
  int iStack_240;
  undefined4 uStack_23c;
  undefined4 local_238;
  undefined4 uStack_234;
  undefined4 local_230;
  undefined1 local_22c [8];
  undefined4 local_224;
  undefined4 local_21c;
  undefined4 uStack_218;
  undefined4 uStack_214;
  undefined4 uStack_210;
  undefined4 local_20c;
  undefined8 local_208;
  undefined4 local_200;
  int *local_1ec;
  int *local_1e8;
  int *local_1e4;
  int *local_1e0;
  int *local_1dc;
  int *local_1d8;
  char local_1d4 [448];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;

  local_8 = 0xffffffff;
  puStack_c = &LAB_00affd56;
  local_10 = ExceptionList;
  uVar4 = DAT_00bf93b4 ^ (uint)&stack0xfffffffc;
  local_294 = param_2;
  if (param_2 < 0) {
    return;
  }
  if (*(int *)(DAT_00c7169c + 0x2a42c) - *(int *)(DAT_00c7169c + 0x2a428) >> 2 <= param_2) {
    return;
  }
  local_36c = *(int *)(*(int *)(DAT_00c7169c + 0x2a428) + param_2 * 4);
  if (local_36c == 0) {
    return;
  }
  ExceptionList = &local_10;
  local_2d0 = param_1;
  local_14 = uVar4;
  FUN_00425ac0(5,param_1);
  local_378 = 2;
  local_29c = *(int **)(DAT_00c7169c + 0x2a3d0);
  if (local_29c == (int *)0x0) {
    local_378 = 900;
  }
  if (DAT_00c71678[0x9961] == 0x20) {
    iVar14 = param_1[0x5e5];
    RNG__Next(uVar4);
    param_2 = *(uint *)(param_2 * 0x10 + iVar14) % 0x61 + 1;
    local_294 = param_2;
  }
  local_2d8 = (code *)(param_3 >> 7 & 0xffffff01);
  local_2ac = param_3 >> 5 & 0xffffff01;
  cVar2 = FUN_007706e0(0x1c3,0);
  if ((cVar2 == '\0') || ((*(int *)(local_36c + 0x58) != 0 && (*(int *)(local_36c + 0x58) != 5)))) {
    local_2a1 = 0;
    bVar3 = ~(byte)(param_3 >> 1) & 1;
LAB_007b23cf:
    local_2a8 = CONCAT31(local_2a8._1_3_,bVar3);
  }
  else {
    local_2dd = 1;
    local_2a1 = 1;
    local_2bc[1] = (int *)(CONCAT31((uint3)(param_3 >> 9),~(byte)(param_3 >> 1)) & 0xffffff01);
    local_2a8 = CONCAT31(local_2a8._1_3_,(char)local_2bc[1]);
    if ((param_3 & 4) != 0) {
      local_2a1 = 1;
      local_2a8 = CONCAT31(local_2a8._1_3_,(char)local_2bc[1]);
      if ((char)local_2ac == '\0') {
        FUN_007b2230(param_2,0x20);
        local_2a1 = local_2dd;
        bVar3 = (byte)local_2bc[1];
        goto LAB_007b23cf;
      }
    }
  }
  local_2de = ~(byte)param_3 & 1;
  piVar5 = (int *)FUN_00753a60(param_2);
  local_298 = piVar5;
  uVar4 = FUN_006eef60();
  if ((((((uVar4 & 1) == 0) && (local_29c == (int *)0x0)) || (local_29c == (int *)0x2)) &&
      ((param_3 & 0x100) == 0)) &&
     (((5 < *DAT_00c71678 - 1U || (cVar2 = BossPool__entry_is_available(0x30), cVar2 == '\0')) &&
      (*DAT_00c71678 != 0xd)))) {
    local_2dd = '\x01';
  }
  else {
    local_2dd = '\0';
  }
  piVar21 = DAT_00c71678;
  switch(local_294) {
  case 1:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    DAT_00c71678[0x60c6] = -1;
    FUN_006fd7c0(piVar21[0x60b4],0xffffffff,3,param_1,0);
    goto LAB_007b8998;
  case 2:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    piVar5 = (int *)FUN_00417170(&DAT_00c34ba0);
    if ((*piVar5 != 0 || piVar5[1] != 0) || (piVar5[2] != 0 || piVar5[3] != 0)) {
      FUN_00929a20(0x185);
    }
    local_3d8 = FUN_0072fd10(0xc0);
    local_3d4 = 0;
    local_3d0 = *(undefined4 *)(local_3d8 + 0x78);
    local_3cc = 0;
    FUN_00930220(&local_3d8,local_2a8,1);
    if (local_2a1 != 0) {
      local_3e8 = FUN_0072fd10(0x22);
      local_3e4 = 0;
      local_3e0 = *(undefined4 *)(local_3e8 + 0x78);
      local_3dc = 0;
      FUN_00930220(&local_3e8,local_2a8,1);
    }
    break;
  case 3:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    local_2d8 = (code *)DAT_00c71678[0x60c0];
    local_2d0 = param_1;
    local_2c8 = param_1;
    if ((*(int *)(local_2d8 + 0x1264) != 0) && (*(int *)(local_2d8 + 0x1bb0) != 6)) {
      local_2b0 = (int *)((uint)local_2b0 & 0xffffff00);
      local_2bc[1] = (int *)0x1;
      local_29c = (int *)0x0;
      if (1 < *(uint *)(local_2d8 + 0x1264)) {
        do {
          piVar5 = *(int **)(*(int *)(local_2d8 + 0x125c) + (int)local_2bc[1] * 4);
          cVar2 = (**(code **)(*param_1 + 0x50))(piVar5);
          if ((cVar2 != '\0') &&
             (((cVar2 = FUN_006ac560(0), cVar2 != '\0' ||
               ((((1 < DAT_00c71678[0x9985] && (piVar5[10] == 1)) ||
                 ((piVar5[10] - 10U < 0x3de && (piVar5[10] != 0x21)))) && ((char)local_2b0 == '\0'))
               )) && ((*(char *)((int)piVar5 + 0x173) == '\0' &&
                      ((float)local_29c <= (float)piVar5[0xe0])))))) {
            local_2d0 = local_2c8;
            local_2c8 = piVar5;
            local_29c = (int *)piVar5[0xe0];
            cVar2 = FUN_006ac560(0);
            local_2b0 = (int *)((uint)local_2b0 & 0xff);
            if (cVar2 != '\0') {
              local_2b0 = (int *)0x1;
            }
          }
          local_2bc[1] = (int *)((int)local_2bc[1] + 1);
        } while (local_2bc[1] < *(int **)(local_2d8 + 0x1264));
      }
    }
    piVar5 = local_2c8;
    if ((local_2d0 == (int *)0x0) || (local_2d0 == param_1)) {
      local_2d0 = local_2c8;
    }
    if (local_2c8 != (int *)0x0) {
      uVar12 = FUN_006eef60();
      local_2a0 = piVar5[0xcf];
      local_29c = (int *)piVar5[0xd0];
      uVar7 = 0;
      pTVar25 = &IsaacRepentancePlus::Entity_Effect::RTTI_Type_Descriptor;
      pTVar24 = &IsaacRepentancePlus::Entity::RTTI_Type_Descriptor;
      uVar11 = 0;
      uVar12 = FUN_00428b20(1000,0x1d,&local_2a0,&DAT_00c7b640,0,0,uVar12);
      piVar5 = (int *)__RTDynamicCast(uVar12,uVar11,pTVar24,pTVar25,uVar7);
      FUN_006a9320(local_2c8);
      (**(code **)(*piVar5 + 0xc))();
    }
    piVar5 = local_2d0;
    if ((local_2a1 != 0) && (local_2d0 != (int *)0x0)) {
      iVar10 = FUN_0060af00(0,0);
      iVar14 = piVar5[0xd0];
      *(int *)(iVar10 + 0x33c) = piVar5[0xcf];
      *(int *)(iVar10 + 0x340) = iVar14;
      FUN_006a9320(piVar5);
    }
    break;
  case 4:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    cVar2 = FUN_009305f0(0x7a);
    if (cVar2 == '\0') {
      FUN_009ad210(3,3,0);
    }
    local_3f8 = FUN_0072fd10(0x7a);
    local_3f4 = 0;
    local_3f0 = *(undefined4 *)(local_3f8 + 0x78);
    local_3ec = 0;
    FUN_00930220(&local_3f8,local_2a8,1);
    if (local_2a1 != 0) {
      local_408 = FUN_0072fd10(0x7a);
      local_404 = 0;
      local_400 = *(undefined4 *)(local_408 + 0x78);
      local_3fc = 0;
      FUN_00930220(&local_408,local_2a8,1);
    }
    break;
  case 5:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    iVar14 = FUN_007484c0(5,0,piVar5,0);
    if (-1 < iVar14) {
      DAT_00c71678[0x60c6] = -1;
      FUN_006fd7c0(iVar14,0xffffffff,3,param_1,0xffffffff);
      local_2de = 0;
    }
    if (local_2a1 != 0) {
      FUN_00424530();
      iVar14 = FUN_00740da0(iVar14,0xffffffff);
      if (*(int *)(iVar14 + 0x40) == 0) {
        FUN_00758d00(2,0);
      }
    }
    break;
  case 6:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    local_29c = (int *)(local_2a1 + 2);
    do {
      uVar12 = RNG__Next();
      FUN_00407480();
      uVar11 = FUN_00813520(local_3a0,param_1 + 0xcf,0x42200000,0,0,0);
      FUN_00428b20(5,10,uVar11,&DAT_00c7b640,param_1,3,uVar12);
      local_29c = (int *)((int)local_29c + -1);
    } while (local_29c != (int *)0x0);
    local_29c = (int *)0x0;
    break;
  case 7:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    local_29c = (int *)(local_2a1 + 2);
    do {
      uVar12 = RNG__Next();
      FUN_00407480();
      uVar11 = FUN_00813520(local_3b8,param_1 + 0xcf,0x42200000,0,0,0);
      FUN_00428b20(5,10,uVar11,&DAT_00c7b640,param_1,1,uVar12);
      local_29c = (int *)((int)local_29c + -1);
    } while (local_29c != (int *)0x0);
    local_29c = (int *)0x0;
    break;
  case 8:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    FUN_0042ca00();
    uVar12 = FUN_0072fd10(0x4d);
    FUN_00435f80(uVar12);
    if (local_2a1 != 0) {
      local_448 = local_448 * 2;
    }
    FUN_00930220(local_450,local_2a8,1);
    break;
  case 9:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    local_29c = (int *)(local_2a1 + 1);
    do {
      cVar2 = FUN_00771550(0x16,0);
      if (cVar2 == '\0') {
LAB_007b2f5b:
        uVar12 = RNG__Next();
        FUN_00407480();
        uVar11 = FUN_00813520(local_3b8,param_1 + 0xcf,0x42200000,0,0,0);
        FUN_00428b20(5,10,uVar11,&DAT_00c7b640,param_1,0,uVar12);
      }
      else {
        FUN_005cbd00(0x16);
        iVar14 = RNG__RandomInt(5);
        if (iVar14 == 0) goto LAB_007b2f5b;
      }
      uVar12 = RNG__Next();
      FUN_00407480();
      uVar11 = FUN_00813520(local_3a0,param_1 + 0xcf,0x42200000,0,0,0);
      FUN_00428b20(5,0x28,uVar11,&DAT_00c7b640,param_1,0,uVar12);
      uVar12 = RNG__Next();
      FUN_00407480();
      uVar11 = FUN_00813520(local_358,param_1 + 0xcf,0x42200000,0,0,0);
      FUN_00428b20(5,0x1e,uVar11,&DAT_00c7b640,param_1,0,uVar12);
      uVar12 = RNG__Next();
      FUN_00407480();
      uVar11 = FUN_00813520(local_344,param_1 + 0xcf,0x42200000,0,0,0);
      FUN_00428b20(5,0x14,uVar11,&DAT_00c7b640,param_1,0,uVar12);
      local_29c = (int *)((int)local_29c + -1);
    } while (local_29c != (int *)0x0);
    local_29c = (int *)0x0;
    break;
  case 10:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    FUN_00424530();
    iVar14 = FUN_007484c0(2,0,piVar5,0);
    if (-1 < iVar14) {
      FUN_00424530();
      FUN_00428ae0(0xffffffff);
      FUN_006fd7c0(iVar14,0xffffffff,3,param_1,0xffffffff);
      if (local_2a1 != 0) {
        FUN_00420ae0();
        FUN_00753c40(2);
      }
      goto LAB_007b8998;
    }
    break;
  case 0xb:
    FUN_006b6470(0x109,2,0,0x3f800000);
    local_2b0 = (int *)0x1;
    iVar14 = FUN_0067f030();
    if (iVar14 == 0) {
      FUN_00421800();
      cVar2 = FUN_00929aa0(0x25f);
      if (cVar2 == '\0') {
LAB_007b319e:
        local_2b0 = (int *)0x3;
      }
      else {
        local_2b0 = (int *)0x10;
      }
    }
    else if (iVar14 < 0x1a) goto LAB_007b319e;
    uVar12 = RNG__Next();
    FUN_00407480();
    uVar11 = FUN_00813520(local_344,param_1 + 0xcf,0x42200000,0,0,0);
    piVar5 = local_2b0;
    goto LAB_007b31f0;
  case 0xc:
    FUN_009302e0(0xc,local_2a8,1);
    iVar14 = FUN_007cae60(0);
    iVar10 = FUN_007cb060();
    if (iVar10 < iVar14) {
      param_1[0x628] = param_1[0x628] + 1;
      FUN_007588a0(2,0);
    }
    FUN_00758a70(2,0,0);
    break;
  case 0xd:
    FUN_0042ca00();
    uVar11 = 1;
    uVar4 = local_2a8;
    uVar12 = FUN_0072fd10(0x14);
    goto LAB_007b327d;
  case 0xe:
    FUN_00456860();
    FUN_009ad210(0xc,0,0);
    FUN_009568e0(0x21,2,0,0x3f800000);
    FUN_005b39d0(&local_2a2,0x23,1,0xffffffff,0);
    FUN_00421800();
    FUN_00929b40(7,1);
    break;
  case 0xf:
    FUN_006b6470(0x109,2,0,0x3f800000);
    uVar12 = RNG__Next();
    FUN_00407480();
    uVar11 = FUN_00813520(local_344,param_1 + 0xcf,0x42200000,0,0,0);
    piVar5 = (int *)0x2;
    goto LAB_007b31f0;
  case 0x10:
    FUN_009568e0(0x22,2,0,0x3f800000);
    FUN_00456860();
    FUN_009ad210(0x22,3,0);
    FUN_0042ca00();
    uVar11 = 1;
    uVar4 = local_2a8;
    uVar12 = FUN_0072fd10(0x22);
    goto LAB_007b327d;
  case 0x11:
    FUN_0042ca00();
    uVar11 = 1;
    uVar4 = local_2a8;
    uVar12 = FUN_0072fd10(0x41);
LAB_007b327d:
    uVar12 = FUN_00435f80(uVar12);
    FUN_00930220(uVar12,uVar4,uVar11);
    break;
  case 0x12:
    FUN_00424530();
    local_2b0 = (int *)FUN_007484c0(0x18,0,piVar5,0);
    if ((int)local_2b0 < 0) {
LAB_007b3428:
      FUN_00424530();
      local_2b0 = (int *)FUN_007484c0(4,0,piVar5,0);
      if ((int)local_2b0 < 0) break;
    }
    else {
      FUN_00424530();
      iVar14 = FUN_00740da0(local_2b0,0xffffffff);
      if (*(int *)(*(int *)(iVar14 + 0x10) + 8) != 0x18) goto LAB_007b3428;
    }
    FUN_00424530();
    FUN_00428ae0(0xffffffff);
    FUN_006fd7c0(local_2b0,0xffffffff,3,param_1,0xffffffff);
    if (local_2a1 != 0) {
      FUN_00420ae0();
      FUN_00753c40(1);
    }
    goto LAB_007b8998;
  case 0x13:
    FUN_00424530();
    uVar11 = 0;
    uVar12 = 7;
    goto LAB_007b34ad;
  case 0x14:
    piVar5 = DAT_00baa454;
    if (local_2a1 != 0) {
      piVar5 = DAT_00baa630;
    }
    local_2c4 = CONCAT44((float)piVar5 * DAT_00baa9d0,(uint)local_2c4);
    FUN_00407480();
    local_2d8 = (code *)FUN_00428a50();
    piVar5 = (int *)0x0;
    local_2bc[1] = (int *)0x0;
    iVar14 = FUN_004176f0();
    if (iVar14 != 0) {
      do {
        puVar13 = (undefined4 *)FUN_00417620(piVar5);
        local_29c = (int *)*puVar13;
        cVar2 = FUN_006ac560(0);
        if (cVar2 != '\0') {
          pcVar20 = *(code **)(*local_29c + 0x20);
          FUN_00431310(param_1);
          (*pcVar20)(local_2c4._4_4_,0,0,local_254,0x1e);
          piVar5 = local_2bc[1];
        }
        piVar5 = (int *)((int)piVar5 + 1);
        local_2bc[1] = piVar5;
        piVar21 = (int *)FUN_004176f0();
      } while (piVar5 < piVar21);
    }
    uVar4 = 0;
    FUN_00417860();
    iVar14 = FUN_00417840();
    if (iVar14 != 0) {
      do {
        FUN_00417860();
        iVar14 = FUN_009b92c0(uVar4);
        if (*(char *)(iVar14 + 0x173) == '\0') {
          FUN_007791f0();
        }
        uVar4 = uVar4 + 1;
        FUN_00417860();
        uVar8 = FUN_00417840();
      } while (uVar4 < uVar8);
    }
    FUN_00424530();
    FUN_007489c0();
    FUN_00407480();
    FUN_005784d0();
    FUN_00424530();
    FUN_00748bc0(1);
    FUN_00456860();
    FUN_009ad210(5,0,0);
    break;
  case 0x15:
    iVar14 = RNG__RandomInt(3);
    if (iVar14 == 0) {
      local_2d0 = (int *)&DAT_00000005;
    }
    else {
      iVar14 = RNG__RandomInt(0x32);
      if (iVar14 == 0) {
        local_2d0 = (int *)&DAT_0000000d;
      }
      else {
        iVar14 = RNG__RandomInt(0x32);
        if (iVar14 == 0) {
          FUN_00421800();
          cVar2 = FUN_00929aa0(0x266);
          if (cVar2 != '\0') {
            local_2d0 = (int *)0x12;
            goto LAB_007b36ff;
          }
        }
        iVar14 = RNG__RandomInt(0x32);
        if (iVar14 == 0) {
          local_2d0 = (int *)&DAT_00000007;
        }
        else {
          iVar14 = RNG__RandomInt(0x32);
          local_2d0 = (int *)&DAT_00000004;
          if (iVar14 == 0) {
            local_2d0 = (int *)&DAT_00000009;
          }
        }
      }
    }
LAB_007b36ff:
    uVar12 = RNG__Next();
    FUN_00407480();
    uVar11 = FUN_00813520(local_344,param_1 + 0xcf,0x42200000,0,0,0);
    piVar5 = local_2d0;
    goto LAB_007b31f0;
  case 0x16:
    FUN_00424530();
    FUN_007489c0();
    break;
  case 0x17:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    iVar14 = param_1[0x4d9];
    if (iVar14 == 0) {
      iVar14 = 2;
    }
    FUN_00759500(iVar14 + (uint)local_2a1 * 2);
    break;
  case 0x18:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    iVar14 = param_1[0x4da];
    if (iVar14 == 0) {
      iVar14 = 2;
    }
    FUN_00759400(iVar14 + (uint)local_2a1 * 2);
    break;
  case 0x19:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    iVar14 = param_1[0x4d7];
    if (iVar14 == 0) {
      iVar14 = 2;
    }
    FUN_007595b0(iVar14 + (uint)local_2a1 * 2);
    break;
  case 0x1a:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    if (param_1[0x4f0] == 0x24) {
      iVar14 = param_1[0x76b];
      if (iVar14 == 0) {
        iVar14 = 2;
      }
      FUN_007d2d40(iVar14 + (uint)local_2a1 * 2);
    }
    else {
      iVar14 = param_1[0x4d1];
      iVar10 = iVar14;
      if (iVar14 == 0) {
        iVar10 = 2;
      }
      local_29c = (int *)((uint)local_2a1 * 2);
      puVar16 = (undefined1 *)((int)local_29c + iVar10);
      if (1 < DAT_00c71678[0x9985]) {
        iVar10 = iVar14;
        if (iVar14 == 0) {
          iVar10 = 0x10;
        }
        uVar4 = iVar10 + (uint)local_2a1 * 0x10;
        puVar16 = (undefined1 *)(uVar4 >> 3);
        param_1[0x4d1] = (uVar4 & 7) + iVar14;
      }
      FUN_00758a70(puVar16,0,0);
    }
    break;
  case 0x1b:
  case 0x1c:
  case 0x1d:
  case 0x1e:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    piVar5 = (int *)DAT_00c71678[0x60c0];
    local_29c = piVar5;
    FUN_00424510();
    local_8 = 0;
    if (piVar5[0x499] != 0) {
      uVar4 = 0;
      do {
        pcVar20 = *(code **)(piVar5[0x497] + uVar4 * 4);
        if (pcVar20[0x173] == (code)0x0) {
          iVar14 = *(int *)(pcVar20 + 0x28);
          if (iVar14 == 5) {
            cVar2 = FUN_006ee200();
            if (((cVar2 != '\0') && (*(int *)(pcVar20 + 0x534) == 0)) &&
               (*(int *)(pcVar20 + 0x2c) != 100)) {
              ppcVar6 = &local_2d8;
              local_2d8 = pcVar20;
LAB_007b2675:
              emplace_back<>(ppcVar6);
            }
          }
          else if ((((((DAT_00c71678[0x9985] < 2) || (iVar14 != 1)) && (iVar14 - 10U < 0x3de)) &&
                    ((iVar14 != 1 && (cVar2 = FUN_006b5b90(0), cVar2 != '\0')))) &&
                   (pcVar20[0x173] == (code)0x0)) && (cVar2 = FUN_006d4db0(), cVar2 != '\0')) {
            local_2c4 = CONCAT44(pcVar20,(uint)local_2c4);
            ppcVar6 = (code **)((int)&local_2c4 + 4);
            goto LAB_007b2675;
          }
        }
        uVar4 = uVar4 + 1;
        piVar5 = local_29c;
        param_1 = local_2d0;
      } while (uVar4 < (uint)local_29c[0x499]);
    }
    local_2bc[1] = (int *)0x0;
    local_2ec = *(int **)(&DAT_00b6bbd8 + local_294 * 4);
    if (local_338 - local_33c >> 2 != 0) {
      do {
        piVar5 = local_2bc[1];
        iVar14 = *(int *)(local_33c + (int)local_2bc[1] * 4);
        if (((1 < DAT_00c71678[0x9985]) && (*(int *)(iVar14 + 0x28) == 1)) ||
           (*(int *)(iVar14 + 0x28) - 10U < 0x3de)) {
          uVar12 = FUN_006eef60();
          iVar14 = *(int *)(local_33c + (int)piVar5 * 4);
          local_2cc = *(undefined4 *)(iVar14 + 0x33c);
          local_2c8 = *(int **)(iVar14 + 0x340);
          FUN_00428b20(1000,0xf,&local_2cc,&DAT_00c7b640,0,0,uVar12);
        }
        piVar21 = *(int **)(local_33c + (int)piVar5 * 4);
        local_29c = (int *)0x0;
        if (piVar21[10] == 5) {
          local_29c = (int *)piVar21[0x14a];
        }
        (**(code **)(*piVar21 + 0x28))();
        iVar14 = *(int *)(local_33c + (int)piVar5 * 4);
        local_2bc[2] = *(int **)(iVar14 + 0x33c);
        local_2b0 = *(int **)(iVar14 + 0x340);
        local_2d4 = *(undefined4 *)(iVar14 + 0x33c);
        local_2d0 = *(int **)(iVar14 + 0x340);
        uVar12 = FUN_00812c90(&local_2d4);
        iVar14 = FUN_007f0800(uVar12);
        if (iVar14 != 0) {
          puVar13 = (undefined4 *)FUN_00813520(local_358,local_2bc + 2,0,0,0,0);
          local_2bc[2] = (int *)*puVar13;
          local_2b0 = (int *)puVar13[1];
        }
        piVar5 = local_2bc[1];
        local_20c = *(undefined4 *)(*(int *)(local_33c + (int)local_2bc[1] * 4) + 0x3ec);
        local_208 = DAT_00b1f4d4;
        local_200 = DAT_00b1f4dc;
        local_8._0_1_ = 1;
        uVar12 = RNG__Next();
        iVar14 = FUN_00428b20(5,local_2ec,local_2bc + 2,&DAT_00c7b640,param_1,0,uVar12);
        local_8 = (uint)local_8._1_3_ << 8;
        local_2bc[1] = (int *)((int)piVar5 + 1);
        *(int **)(iVar14 + 0x528) = local_29c;
      } while (local_2bc[1] < (int *)(local_338 - local_33c >> 2));
    }
    local_8 = 0xffffffff;
    FID_conflict__Tidy();
    break;
  case 0x1f:
    DAT_00c71678[0x60c6] = -1;
    uVar12 = FUN_007484c0(0xe,0,piVar5,0);
    FUN_006fd7c0(uVar12,0xffffffff,3,param_1,0);
    goto LAB_007b8998;
  case 0x20:
    FUN_005b23f0(0);
    break;
  case 0x21:
    FUN_00407480();
    FUN_00428a60();
    FUN_0041af60(local_3b0,5,0xffffffff,0xffffffff,0,0);
    local_8 = 3;
    piVar5 = (int *)0x0;
    local_2bc[1] = (int *)0x0;
    iVar14 = FUN_004176f0();
    if (iVar14 != 0) {
      do {
        FUN_00417620(piVar5);
        cVar2 = FUN_006ee3f0();
        if (cVar2 != '\0') {
          puVar13 = (undefined4 *)FUN_00417620(piVar5);
          local_29c = (int *)*puVar13;
          local_2d8 = (code *)FUN_00505b70();
          uVar12 = FUN_00417280();
          FUN_00407480();
          uVar11 = FUN_00417290(local_330);
          uVar11 = FUN_00813520(local_31c,uVar11,0x42200000,0,0,0);
          uVar7 = FUN_00417270();
          param_1 = local_2d0;
          FUN_00428b20(5,uVar7,uVar11,&DAT_00c7b640,local_2d0,uVar12,local_2d8);
          piVar5 = local_2bc[1];
        }
        piVar5 = (int *)((int)piVar5 + 1);
        local_2bc[1] = piVar5;
        piVar21 = (int *)FUN_004176f0();
      } while (piVar5 < piVar21);
    }
    FUN_00456860();
    FUN_009ad210(0x15,4,0);
    local_8 = 0xffffffff;
    FUN_004175b0();
    break;
  case 0x22:
    FUN_005b39d0((int)&local_2f8 + 2,0x54,1,0xffffffff,0);
    FUN_00456860();
    FUN_009ad210(0x16,4,0);
    break;
  case 0x23:
    FUN_00424530();
    FUN_00748bc0(0xffffffff);
    FUN_00758d00(2,0);
    FUN_00456860();
    FUN_009ad210(0x17,4,0);
    FUN_00417850();
    cVar2 = FUN_00429550();
    if (cVar2 != '\0') {
      FUN_0042ca00();
      uVar12 = FUN_0072fd10(0x278);
      FUN_00435f80(uVar12);
      local_478 = 600;
      FUN_00930220(local_480,1,1);
    }
    break;
  case 0x24:
    FUN_00424530();
    FUN_007489c0();
    FUN_00424530();
    FUN_007488d0();
    FUN_00456860();
    FUN_009ad210(0x18,4,0);
    break;
  case 0x25:
    FUN_005b39d0((int)&local_2f8 + 2,0x69,1,0xffffffff,0);
    FUN_00456860();
    FUN_009ad210(0x19,4,0);
    break;
  case 0x26:
    iVar14 = 3;
    do {
      uVar12 = FUN_006eef60();
      FUN_00428b20(3,0xe7,param_1 + 0xcf,&DAT_00c7b640,param_1,0x19,uVar12);
      FUN_005b18f0(1);
      iVar14 = iVar14 + -1;
    } while (iVar14 != 0);
    FUN_00456860();
    FUN_009ad210(0x1a,4,0);
    break;
  case 0x27:
    FUN_0042ca00();
    uVar12 = FUN_0072fd10(0x3a);
    FUN_00435f80(uVar12);
    local_468 = 600;
    FUN_00930220(local_470,local_2a8,1);
    FUN_00456860();
    FUN_009ad210(0x1b,4,0);
    break;
  case 0x28:
    iVar14 = RNG__RandomInt(4);
    if ((iVar14 == 0) && ((char)local_2d8 == '\0')) {
      uVar12 = RNG__Next();
      FUN_00407480();
      uVar11 = FUN_00813520(local_330,param_1 + 0xcf,0x42200000,0,0,0);
      FUN_00428b20(5,300,uVar11,&DAT_00c7b640,param_1,0x28,uVar12);
    }
    iVar14 = RNG__RandomInt(9);
    local_2b0 = *(int **)(&DAT_00b6bc20 + iVar14 * 4);
    FUN_00417850();
    cVar2 = FUN_00429550();
    if (cVar2 != '\0') {
      FUN_00417850();
      piVar5 = (int *)FUN_004176f0();
      cVar2 = (**(code **)(*piVar5 + 0x24))(local_2b0);
      while (cVar2 != '\0') {
        iVar14 = RNG__RandomInt(9);
        piVar5 = *(int **)(&DAT_00b6bc20 + iVar14 * 4);
        local_2b0 = piVar5;
        FUN_00417850();
        piVar21 = (int *)FUN_004176f0();
        cVar2 = (**(code **)(*piVar21 + 0x24))(piVar5);
        param_1 = local_2d0;
      }
    }
    FUN_007b2230(local_2b0,0);
    break;
  case 0x29:
    if (((param_1[0x5f1] != 0) && (cVar2 = FUN_005b14e0(), cVar2 != '\0')) &&
       (cVar2 = FUN_005b1500(0x8000,0), cVar2 == '\0')) {
      local_1ec = param_1 + 0x548;
      param_1[0x5f1] = 0;
      local_1e8 = param_1 + 0x549;
      param_1[0x5f2] = 0;
      local_1e4 = param_1 + 0x54a;
      local_1e0 = param_1 + 0x54b;
      local_1dc = param_1 + 0x54c;
      local_1d8 = param_1 + 0x54d;
      uVar12 = FUN_005cbd00(0x29);
      FUN_005cbfe0(uVar12);
      *local_1ec = *local_1ec + 1;
      *local_1e8 = *local_1e8 + 1;
      uVar12 = FUN_006eef60();
      param_1 = local_2d0;
      uVar11 = FUN_00a0fe90();
      uVar11 = FUN_00a10420(local_31c,uVar11);
      FUN_00428b20(1000,0xf,uVar11,&DAT_00c7b640,0,0,uVar12);
    }
    FUN_00407480();
    local_2b0 = (int *)FUN_00428a50();
    local_2a1 = 0;
    FUN_00424510();
    local_8 = 4;
    piVar5 = (int *)0x0;
    local_2c8 = (int *)0x0;
    iVar14 = FUN_004176f0();
    if (iVar14 != 0) {
      do {
        FUN_00417620(piVar5);
        local_298 = (int *)FUN_00435e30();
        if (((local_298 != (int *)0x0) && (cVar2 = FUN_005b1930(), cVar2 == '\0')) &&
           ((cVar2 = FUN_00417470(), cVar2 == '\0' && (cVar2 = FUN_006ee200(), cVar2 != '\0')))) {
          iVar14 = FUN_00417270();
          if (((iVar14 == 100) && (iVar14 = FUN_00417280(), iVar14 != 0)) &&
             (iVar14 = FUN_005b1940(), iVar14 < 1)) {
            local_1ec = param_1 + 0x548;
            local_2a1 = 1;
            local_1e8 = param_1 + 0x549;
            local_1e4 = param_1 + 0x54a;
            local_1e0 = param_1 + 0x54b;
            local_1dc = param_1 + 0x54c;
            local_1d8 = param_1 + 0x54d;
            uVar12 = FUN_005cbd00(0x29);
            FUN_005cbfe0(uVar12);
            *local_1ec = *local_1ec + 1;
            *local_1e8 = *local_1e8 + 1;
            uVar12 = FUN_006eef60();
            FUN_00417290(local_330);
            uVar11 = FUN_00a0fe90();
            uVar11 = FUN_00a10420(local_360,uVar11);
            FUN_00428b20(1000,0xf,uVar11,&DAT_00c7b640,0,0,uVar12);
            FUN_0060d1f0(4);
            FUN_006ee750();
            iVar14 = FUN_005b1960();
            if (iVar14 != -1) {
              FUN_00417860();
              uVar4 = FUN_009bfa00();
              if (iVar14 + 1U < uVar4) {
                FUN_0042c850(&local_298);
              }
            }
          }
          else {
            iVar14 = FUN_00417270();
            if ((iVar14 != 100) && (cVar2 = FUN_006ee200(), cVar2 != '\0')) {
              (**(code **)(*local_298 + 0x28))();
              uVar11 = 0;
              uVar12 = FUN_00417290(local_368);
              FUN_007599d0(1,uVar12,uVar11);
            }
          }
        }
        piVar19 = (int *)((int)local_2c8 + 1);
        local_2c8 = piVar19;
        piVar21 = (int *)FUN_004176f0();
        piVar5 = local_2c8;
        param_1 = local_2d0;
      } while (piVar19 < piVar21);
    }
    piVar5 = (int *)0x0;
    local_2bc[1] = (int *)0x0;
    iVar14 = FUN_00417840();
    if (iVar14 != 0) {
      local_29c = local_2d0 + 0xf7;
      do {
        puVar13 = (undefined4 *)FUN_0042c810(piVar5);
        piVar5 = (int *)*puVar13;
        iVar14 = FUN_005b1960();
        FUN_00417290(local_2dc);
        (**(code **)(*piVar5 + 0x28))();
        FUN_0042a330();
        uVar12 = RNG__Next();
        uVar12 = FUN_00733610(2,uVar12,0,0,0);
        uVar11 = RNG__Next();
        piVar5 = (int *)FUN_00428b20(5,100,local_2dc,&DAT_00c7b640,0,uVar12,uVar11);
        FUN_006e2ff0(iVar14 + 1);
        (**(code **)(*piVar5 + 0xc))();
        piVar5 = (int *)((int)local_2bc[1] + 1);
        local_2bc[1] = piVar5;
        piVar21 = (int *)FUN_00417840();
      } while (piVar5 < piVar21);
    }
    FUN_007dc610();
    param_1 = local_2d0;
    local_2d0[0x55d] = local_2d0[0x55d] | 0x41f;
    FUN_00763570();
    FUN_005b39d0((int)&local_2f8 + 2,0x23,1,0xffffffff,0);
    if (local_2a1 != 0) {
      FUN_00407480();
      iVar14 = FUN_0043eec0();
      if (iVar14 != 0xb) {
        FUN_00407480();
        iVar14 = FUN_0043eec0();
        if (iVar14 != 0x11) goto LAB_007b4865;
      }
      FUN_005b1860();
      FUN_00833420();
    }
LAB_007b4865:
    local_8 = 0xffffffff;
    FID_conflict__Tidy();
    break;
  case 0x2a:
    local_2d8 = (code *)(param_1 + 0x598);
    FUN_00a10030(local_2f0);
    cVar2 = FUN_00a10600(&DAT_00c7b640);
    if (cVar2 != '\0') {
      FUN_007dd3b0(param_1 + 0x591);
    }
    cVar2 = FUN_00a10600(&DAT_00c7b640);
    if (cVar2 != '\0') {
      uVar12 = FUN_00a0fe90();
      FUN_007dd3b0(uVar12);
    }
    uVar12 = FUN_006eef60();
    local_29c = (int *)0x41200000;
    FUN_00a104e0(local_398,&local_29c);
    local_2bc[1] = (int *)0x3f000000;
    FUN_00a104e0(local_368,local_2bc + 1);
    local_2c4 = CONCAT44(0x40000000,(uint)local_2c4);
    uVar11 = FUN_00a104e0(local_360,(int)&local_2c4 + 4);
    uVar11 = FUN_00a10420(local_31c,uVar11);
    param_1 = local_2d0;
    FUN_00428b20(2,9,local_2d0 + 0xcf,uVar11,local_2d0,0,uVar12);
    goto LAB_007b8998;
  case 0x2b:
    FUN_00407480();
    FUN_00428a60();
    FUN_0041af60(local_418,5,0xffffffff,0xffffffff,0,0);
    local_8 = 2;
    uVar4 = 0;
    iVar14 = FUN_004176f0();
    if (iVar14 != 0) {
      do {
        puVar13 = (undefined4 *)FUN_00417620(uVar4);
        local_29c = (int *)__RTDynamicCast(*puVar13,0,
                                           &IsaacRepentancePlus::Entity::RTTI_Type_Descriptor,
                                           &IsaacRepentancePlus::Entity_Pickup::RTTI_Type_Descriptor
                                           ,0);
        if ((local_29c != (int *)0x0) && (iVar14 = FUN_00431740(), iVar14 != 0)) {
          FUN_006e2570(0);
        }
        uVar4 = uVar4 + 1;
        uVar8 = FUN_004176f0();
      } while (uVar4 < uVar8);
    }
    local_8 = 0xffffffff;
    FUN_004175b0();
    break;
  case 0x2c:
    fVar22 = (float10)RNG__RandomFloat();
    local_29c = (int *)(float)fVar22;
    if (DAT_00baa0d0 <= (float)local_29c) {
      FUN_00753d00();
    }
    else {
      FUN_0065d070();
    }
    break;
  case 0x2d:
    FUN_006b6470(0x25,2,0,0x3f800000);
    FUN_00407480();
    FUN_007537d0();
    break;
  case 0x2e:
    pcVar20 = *(code **)(*param_1 + 0x24);
    uVar12 = FUN_00435c70();
    (*pcVar20)(uVar12);
    param_1[0x5aa] = 0;
    param_1[0x5ab] = 0;
    param_1[0x59f] = 0;
    param_1[0x5a0] = 0;
    local_29c = (int *)0x0;
    do {
      uVar12 = RNG__Next();
      FUN_00407480();
      uVar11 = FUN_00813520(local_344,param_1 + 0xcf,0x42200000,0,0,0);
      iVar14 = RNG__RandomInt(0xc);
      param_1 = local_2d0;
      FUN_00428b20(5,*(undefined4 *)(&DAT_00b6bbf0 + iVar14 * 4),uVar11,&DAT_00c7b640,local_2d0,0,
                   uVar12);
      piVar5 = local_29c;
      FUN_005b19f0(local_29c);
      local_29c = (int *)((int)piVar5 + 1);
    } while ((int)local_29c < 10);
    goto LAB_007b8998;
  case 0x2f:
    FUN_005b39d0(&local_2a2,0xaf,1,0xffffffff,0);
    break;
  case 0x30:
    iVar14 = param_1[0x560];
    if (iVar14 != 0) {
      if (iVar14 != 0x11e) {
        if (((iVar14 == 0x1a6) && (iVar14 = FUN_00706780(), iVar14 != 0)) &&
           ((-1 < param_1[0x588] && (iVar14 = FUN_00706780(), iVar14 != 0)))) {
          local_29c = (int *)(param_1[0x588] * 0x5dc + 0x19d80 + iVar14);
          local_2b0 = (int *)0x0;
          piVar5 = local_29c + 0x41;
LAB_007b3be0:
          cVar2 = FUN_00753630();
          if ((cVar2 == '\0') || (*piVar5 != 0x30)) goto LAB_007b3bf0;
          if (local_2b0 < (int *)0x3) {
            piVar5 = local_29c + (int)local_2b0 * 2 + 0x43;
            piVar21 = local_29c + (int)local_2b0 * 2 + 0x41;
            for (uVar4 = (3 - (int)local_2b0) * 2 & 0x3ffffffe; param_1 = local_2d0, uVar4 != 0;
                uVar4 = uVar4 - 1) {
              *piVar21 = *piVar5;
              piVar5 = piVar5 + 1;
              piVar21 = piVar21 + 1;
            }
          }
          FUN_00753620();
        }
LAB_007b3c4c:
        FUN_005b39d0((int)&local_2f8 + 2,param_1[0x560],4,0,0);
        FUN_005ca470(param_1[0x560],0);
        goto LAB_007b8998;
      }
      FUN_00424530();
      cVar2 = FUN_0074b710();
      if (cVar2 == '\0') {
        uVar12 = FUN_006eef60();
        FUN_00407480();
        uVar11 = FUN_00813520(local_31c,param_1 + 0xcf,0,0,0,0);
        FUN_00428b20(0x11,2,uVar11,&DAT_00c7b640,param_1,0,uVar12);
      }
      else {
        FUN_00424530();
        FUN_00428ae0(0xffffffff);
        FUN_006fd7c0(0xfffffffe,0xffffffff,3,param_1,0xffffffff);
      }
      FUN_0078f840(param_1[0x560],0,0,1);
    }
    break;
  case 0x31:
    FUN_005b39d0(&local_2a2,0x69,1,0xffffffff,0);
    FUN_005b39d0((int)&local_2f8 + 2,0xa6,1,0xffffffff,0);
    break;
  case 0x32:
    FUN_00407480();
    local_29c = (int *)FUN_00428a50();
    piVar5 = (int *)0x0;
    local_2c4 = 0;
    local_2b0 = (int *)0x0;
    iVar14 = FUN_004176f0();
    if (iVar14 != 0) {
      do {
        FUN_00417620(piVar5);
        cVar2 = FUN_006ac560(0);
        if (cVar2 != '\0') {
          if ((uint)local_2c4 == 0) {
            puVar13 = (undefined4 *)FUN_00417620(piVar5);
            local_2c4 = CONCAT44(local_2c4._4_4_,*puVar13);
          }
          else {
            if (local_2c4._4_4_ != (int *)0x0) {
              local_2d8 = (code *)FUN_00417290(local_31c);
              local_2bc[1] = (int *)FUN_00417290(local_360);
              FUN_00417620(piVar5);
              FUN_00417290(local_368);
              uVar12 = FUN_00417290(local_398);
              fVar22 = (float10)FUN_00a0ff90(local_2bc[1]);
              local_2d8 = (code *)(float)fVar22;
              fVar22 = (float10)FUN_00a0ff90(uVar12);
              local_2bc[1] = (int *)(float)fVar22;
              piVar5 = local_2b0;
              if ((float)local_2bc[1] <= (float)local_2d8) goto LAB_007b3d9f;
            }
            puVar13 = (undefined4 *)FUN_00417620(piVar5);
            local_2c4 = CONCAT44(*puVar13,(uint)local_2c4);
          }
        }
LAB_007b3d9f:
        piVar5 = (int *)((int)piVar5 + 1);
        local_2b0 = piVar5;
        piVar21 = (int *)FUN_004176f0();
      } while (piVar5 < piVar21);
    }
    local_29c = (int *)0x0;
    do {
      local_2bc[1] = *(int **)((int)&local_2c4 + (int)local_29c * 4);
      if (local_2bc[1] != (int *)0x0) {
        uVar12 = FUN_006eef60();
        FUN_00417290(local_31c);
        uVar11 = FUN_00a0fe90();
        uVar11 = FUN_00a10420(local_368,uVar11);
        uVar26 = 0;
        pTVar25 = &IsaacRepentancePlus::Entity_Effect::RTTI_Type_Descriptor;
        pTVar24 = &IsaacRepentancePlus::Entity::RTTI_Type_Descriptor;
        uVar7 = 0;
        uVar12 = FUN_00428b20(1000,0x5b,uVar11,&DAT_00c7b640,0,0,uVar12);
        piVar21 = (int *)__RTDynamicCast(uVar12,uVar7,pTVar24,pTVar25,uVar26);
        piVar5 = local_2bc[1];
        FUN_006a9320(local_2bc[1]);
        FUN_00435e90(0x96);
        (**(code **)(*piVar21 + 0xc))();
        __RTDynamicCast(piVar5,0,&IsaacRepentancePlus::Entity::RTTI_Type_Descriptor,
                        &IsaacRepentancePlus::Entity_NPC::RTTI_Type_Descriptor,0);
        uVar12 = FUN_00417290(local_330);
        FUN_006b5e20(0x96,uVar12);
      }
      local_29c = (int *)((int)local_29c + 1);
      param_1 = local_2d0;
    } while ((int)local_29c < 2);
    break;
  case 0x33:
    cVar2 = FUN_00930680(0x2e);
    uVar4 = local_2a8;
    if (cVar2 == '\0') {
      FUN_00930390(0x2e,local_2a8,1);
      FUN_009302e0(0x139,uVar4,1);
    }
    break;
  case 0x34:
    FUN_00703670(0x1e);
    FUN_0042ca00();
    uVar12 = FUN_0072fda0(0x29);
    cVar2 = FUN_009305c0(uVar12);
    if (cVar2 == '\0') {
      FUN_0042ca00();
      uVar12 = FUN_0072fda0(0x29);
      FUN_00435f80(uVar12);
      FUN_00930220(local_390,local_2a8,1);
      FUN_009302e0(0x12e,0,1);
    }
    break;
  case 0x35:
    FUN_00407480();
    FUN_00813520(local_380,param_1 + 0xcf,0,0,0,0);
    local_29c = param_1 + 0x5e5;
    local_2b0 = (int *)0x0;
    do {
      uVar12 = RNG__Next();
      FUN_0042a330();
      FUN_005cbd00(0x35);
      uVar11 = RNG__Next();
      uVar11 = FUN_00734870(uVar11,1,0,0);
      FUN_00a10350(local_374,(float)(int)local_2b0 * DAT_00baae50);
      local_2d8 = (code *)0x40000000;
      uVar7 = FUN_00a104e0(local_300,&local_2d8);
      param_1 = local_2d0;
      FUN_00428b20(5,300,local_380,uVar7,local_2d0,uVar11,uVar12);
      local_2b0 = (int *)((int)local_2b0 + 1);
    } while ((int)local_2b0 < 3);
    break;
  case 0x36:
    FUN_0042ca00();
    uVar12 = FUN_0072fda0(0x2a);
    FUN_00435f80(uVar12);
    FUN_00930220(local_390,1,1);
    FUN_00407480();
    FUN_004360d0();
    FUN_009302e0(0xe8,1,1);
    break;
  case 0x37:
    local_2b0 = (int *)RNG__RandomInt(8);
    FUN_00417850();
    cVar2 = FUN_00429550();
    piVar21 = local_2b0;
    while ((cVar2 != '\0' &&
           ((piVar21 == (int *)0x0 || (param_1 = local_2d0, piVar21 == (int *)&DAT_00000006))))) {
      piVar21 = (int *)RNG__RandomInt(8);
      local_2b0 = piVar21;
      FUN_00417850();
      cVar2 = FUN_00429550();
      param_1 = local_2d0;
    }
    switch(local_2b0) {
    case (int *)0x0:
      local_2d8 = (code *)FUN_00424530();
      uVar4 = FUN_004360e0();
      if ((-1 < (int)uVar4) && (uVar4 < 0xa9)) {
        piVar5 = (int *)((int)uVar4 / 0xd);
        local_2bc[1] = (int *)((int)uVar4 % 0xd);
        local_298 = (int *)((int)local_2bc[1] + -3);
        local_2c4 = CONCAT44((undefined1 *)((int)local_2bc[1] + 3),(uint)local_2c4);
        local_2b0 = piVar5;
        if ((int)local_298 <= (int)local_2bc[1] + 3) {
          local_2c8 = (int *)0xfffffffd;
          do {
            piVar21 = local_2c8;
            if (((undefined1 *)((int)local_2bc[1] + (int)local_2c8) < (undefined1 *)0xd) &&
               ((int)piVar5 + -3 <= (int)((int)piVar5 + 3))) {
              uVar4 = 0xfffffffd;
              local_29c = (int *)0x7;
              puVar16 = (undefined1 *)((int)((int)piVar5 + -3) * 0xd + (int)local_298);
              do {
                if ((((undefined1 *)(uVar4 + (int)piVar5) < (undefined1 *)0xd) &&
                    (uVar17 = (int)piVar21 >> 0x1f, uVar8 = (uint)piVar21 ^ uVar17,
                    piVar5 = local_2b0, piVar21 = local_2c8,
                    (int)((uVar8 - uVar17) + ((uVar4 ^ (int)uVar4 >> 0x1f) - ((int)uVar4 >> 0x1f)))
                    < 4)) && (iVar14 = FUN_00740da0(puVar16,0xffffffff), piVar5 = local_2b0,
                             piVar21 = local_2c8, *(int *)(iVar14 + 0x10) != 0)) {
                  *(uint *)(iVar14 + 0x3c) = *(uint *)(iVar14 + 0x3c) | 5;
                }
                uVar4 = uVar4 + 1;
                puVar16 = puVar16 + 0xd;
                local_29c = (int *)((int)local_29c + -1);
              } while (local_29c != (int *)0x0);
              local_29c = (int *)0x0;
            }
            local_298 = (int *)((int)local_298 + 1);
            local_2c8 = (int *)((int)piVar21 + 1);
            param_1 = local_2d0;
          } while ((int)local_298 <= (int)local_2c4._4_4_);
        }
      }
      FUN_00738380();
      FUN_0098db50();
      break;
    case (int *)0x1:
      FUN_0042a330();
      FUN_00736f90();
      FUN_00407480();
      FUN_00428a60();
      FUN_0041af60(local_428,5,100,0xffffffff,0,0);
      local_8 = 5;
      uVar11 = 0xb;
      local_298 = (int *)0x0;
      uVar12 = FUN_0040c3a0(0xb);
      RNG__game_constructor(uVar12,uVar11);
      local_8 = CONCAT31(local_8._1_3_,6);
      iVar14 = RNG__RandomInt(2);
      local_29c = (int *)((-(uint)(iVar14 != 0) & 0xffffffdc) + 0x24);
      iVar14 = FUN_004176f0();
      if (iVar14 != 0) {
        uVar4 = 0;
        do {
          puVar13 = (undefined4 *)FUN_00417620(uVar4);
          uVar12 = *puVar13;
          cVar2 = FUN_00417470();
          if ((cVar2 == '\0') && (iVar14 = FUN_00417280(), iVar14 != 0)) {
            piVar5 = (int *)__RTDynamicCast(uVar12,0,&IsaacRepentancePlus::Entity::
                                                      RTTI_Type_Descriptor,
                                            &IsaacRepentancePlus::Entity_Pickup::
                                             RTTI_Type_Descriptor,0);
            cVar2 = FUN_006ee200();
            if (((cVar2 != '\0') &&
                ((iVar14 = FUN_005b1980(), iVar14 == 0 || (iVar14 = FUN_005b1940(), iVar14 < 0))))
               && ((iVar14 = RNG__Next(), local_298 == (int *)0x0 || (iVar14 != 0)))) {
              local_298 = piVar5;
            }
          }
          piVar5 = local_298;
          uVar4 = uVar4 + 1;
          uVar8 = FUN_004176f0();
          param_1 = local_2d0;
        } while (uVar4 < uVar8);
        if (piVar5 != (int *)0x0) {
          uVar12 = FUN_00417270();
          uVar11 = FUN_00417260();
          FUN_006e30a0(uVar11,uVar12,local_29c,1,0,0);
          FUN_005b1950(0);
        }
      }
      guard_check_icall();
      local_8 = 0xffffffff;
      FUN_004175b0();
      break;
    case (int *)0x2:
      uVar12 = FUN_006eef60();
      FUN_00428b20(3,0xe7,param_1 + 0xcf,&DAT_00c7b640,param_1,0x19,uVar12);
      FUN_005b18f0(1);
      break;
    case (int *)0x3:
      FUN_0042ca00();
      uVar12 = FUN_0072fd10(0x3a);
      FUN_00435f80(uVar12);
      local_224 = 0x5a;
      FUN_00930220(local_22c,local_2a8,1);
      break;
    case (int *)0x4:
      FUN_005b23f0(piVar5);
      break;
    case (int *)0x5:
      FUN_005b39d0((int)&local_30c + 2,0x1dc,1,0xffffffff,0);
      break;
    case (int *)0x6:
      FUN_005b39d0((int)&local_310 + 2,0x54,1,0xffffffff,0);
      break;
    case (int *)0x7:
      FUN_00758d00(1,0);
    }
    break;
  case 0x38:
    iVar14 = 0;
    local_2bc[0] = param_1;
    uVar4 = 0;
    local_2bc[1] = (int *)param_1[0x766];
    piVar5 = (int *)0x0;
    local_310 = 0;
    local_2f4 = (int *)0x0;
    local_2b0 = (int *)0x0;
    local_2f8 = 0;
    local_2c8 = (int *)0x0;
    local_30c = 0;
    local_2a8 = 0;
    local_29c = (int *)0x0;
    do {
      piVar21 = local_2bc[(int)local_29c];
      if (piVar21 != (int *)0x0) {
        local_2f8 = local_2f8 + piVar21[0x4d2];
        local_2c8 = (int *)((int)local_2c8 + piVar21[0x653]);
        local_2ec = (int *)piVar21[0x769];
        local_2ac = piVar21[0x4d1];
        piVar21[0x4d2] = 0;
        piVar21[0x653] = 0;
        local_2e8 = (int *)FUN_00759260();
        local_2e4 = (int *)piVar21[0x4d3];
        local_2c4 = CONCAT44(piVar21[0x762],(uint)local_2c4);
        if ((piVar21[0x4d1] < 1) || (piVar21[0x4d0] < 1)) {
          if (piVar21[0x762] < 1) {
            if (0 < (int)local_2e4) {
              FUN_00758d00(1 - (int)local_2e4,0);
            }
          }
          else {
            FUN_00758a70(-piVar21[0x4d1],0,0);
            FUN_00758d00(-piVar21[0x4d3],0);
            piVar21[0x762] = 1;
            FUN_007cabc0();
          }
        }
        else {
          iVar10 = FUN_007cafe0();
          iVar14 = piVar21[0x4d1];
          if (iVar10 == 3) {
            if (2 < iVar14) {
              iVar10 = 2;
LAB_007b4f9f:
              FUN_00758a70(iVar10 - iVar14,0,0);
            }
          }
          else if (1 < iVar14) {
            iVar10 = 1;
            goto LAB_007b4f9f;
          }
          FUN_00758d00(-piVar21[0x4d3],0);
          piVar21[0x762] = 0;
          FUN_007cabc0();
        }
        local_2ec = (int *)((int)local_2ec - piVar21[0x769]);
        local_2ac = (local_2ac + (int)local_2ec * -2) - piVar21[0x4d1];
        iVar14 = FUN_00759260();
        local_2e8 = (int *)((int)local_2e8 - iVar14);
        local_2e4 = (int *)(((int)local_2e4 + (int)local_2e8 * -2) - piVar21[0x4d3]);
        if ((0 < (int)local_2ac) && (iVar14 = FUN_007cafe0(), iVar14 == 3)) {
          iVar14 = local_2ac + 1;
          local_2ac = 0;
          local_2a8 = local_2a8 + iVar14 / 2;
        }
        piVar5 = local_2e4;
        if ((int)local_2e4 < 0) {
          iVar14 = (1 - (int)local_2e4) / 2;
          local_2e8 = (int *)((int)local_2e8 - iVar14);
          piVar5 = (int *)((int)local_2e4 + iVar14 * 2);
        }
        iVar14 = (int)local_2c4._4_4_ - piVar21[0x762];
        uVar4 = uVar4 + local_2ac;
        local_2c4 = CONCAT44(iVar14,(uint)local_2c4);
        local_310 = local_310 + (int)local_2ec;
        local_2b0 = (int *)((int)local_2b0 + (int)local_2e8);
        piVar5 = (int *)((int)local_2f4 + (int)piVar5);
        local_30c = local_30c + iVar14;
        iVar14 = local_2a8;
        local_2f4 = piVar5;
      }
      param_1 = local_2d0;
      local_29c = (int *)((int)local_29c + 1);
    } while (local_29c < (int *)0x2);
    if (0 < local_2d0[0x76a]) {
      local_2f4 = (int *)((int)piVar5 + local_2d0[0x76a]);
      local_2d0[0x76a] = 0;
    }
    uVar8 = uVar4;
    if (0 < local_2d0[0x76b]) {
      uVar8 = uVar4 + local_2d0[0x76b];
      local_2d0[0x76b] = 0;
    }
    local_2a8 = iVar14 + local_2d0[0x4da];
    local_2bc[1] = (int *)local_2d0[0x775];
    local_2d8 = (code *)(uint)(*(char *)((int)local_2d0 + 0x1361) != '\0');
    local_2e4 = (int *)(local_2d0[0x4d9] - (int)local_2bc[1]);
    local_2e8 = (int *)local_2d0[0x4d7];
    local_2d0[0x4da] = 0;
    local_29c = (int *)(uint)((char)local_2d0[0x4d8] != '\0');
    local_2d0[0x4d9] = 0;
    local_2d0[0x775] = 0;
    *(undefined1 *)((int)local_2d0 + 0x1361) = 0;
    local_2d0[0x4d7] = 0;
    *(undefined1 *)(local_2d0 + 0x4d8) = 0;
    local_2ac = uVar4;
    FUN_005b19d0();
    uVar11 = 0x2c;
    uVar12 = RNG__Next(0x2c);
    RNG__game_constructor(uVar12,uVar11);
    local_8 = 7;
    local_2ec = param_1 + 0xcf;
    while (0 < (int)uVar8) {
      iVar14 = FUN_007dd380();
      if ((int)uVar8 < iVar14) {
        iVar14 = FUN_007dd380();
        if ((int)uVar8 < iVar14) {
          local_2c4 = CONCAT44(2,(uint)local_2c4);
        }
        else {
          local_2c4 = CONCAT44(1,(uint)local_2c4);
        }
      }
      else {
        local_2c4 = CONCAT44(5,(uint)local_2c4);
      }
      iVar14 = FUN_007dd380();
      local_2ac = uVar8 - iVar14;
      uVar12 = RNG__Next();
      FUN_00407480();
      uVar11 = FUN_00813520(local_300,param_1 + 0xcf,0x42200000,0,0,0);
      FUN_00428b20(5,10,uVar11,&DAT_00c7b640,param_1,local_2c4._4_4_,uVar12);
      uVar8 = local_2ac;
    }
    local_2c4._4_4_ = param_1 + 0xcf;
    iVar14 = local_310;
    piVar5 = local_2f4;
    if (0 < local_310) {
      do {
        uVar12 = RNG__Next();
        FUN_00407480();
        uVar11 = FUN_00813520(local_300,local_2c4._4_4_,0x42200000,0,0,0);
        FUN_00428b20(5,10,uVar11,&DAT_00c7b640,param_1,0xc,uVar12);
        local_310 = local_310 + -1;
        iVar14 = 0;
        piVar5 = local_2f4;
      } while (local_310 != 0);
    }
    while (local_310 = iVar14, local_2f4 = piVar5, 0 < (int)piVar5) {
      iVar14 = FUN_007dd380();
      if ((int)piVar5 < iVar14) {
        local_2c4._4_4_ = (int *)&DAT_00000008;
      }
      else {
        local_2c4._4_4_ = (int *)0x3;
      }
      iVar14 = FUN_007dd380();
      local_2f4 = (int *)((int)piVar5 - iVar14);
      uVar12 = RNG__Next();
      FUN_00407480();
      uVar11 = FUN_00813520(local_300,param_1 + 0xcf,0x42200000,0,0,0);
      FUN_00428b20(5,10,uVar11,&DAT_00c7b640,param_1,local_2c4._4_4_,uVar12);
      iVar14 = local_310;
      piVar5 = local_2f4;
    }
    local_2c4 = (ulonglong)(uint)local_2c4;
    iVar14 = FUN_007dd380();
    if (0 < iVar14) {
      do {
        uVar12 = RNG__Next();
        FUN_00407480();
        uVar11 = FUN_00813520(local_300,param_1 + 0xcf,0x42200000,0,0,0);
        FUN_00428b20(5,10,uVar11,&DAT_00c7b640,param_1,6,uVar12);
        iVar10 = (int)local_2c4._4_4_ + 1;
        local_2c4 = CONCAT44(iVar10,(uint)local_2c4);
        iVar14 = FUN_007dd380();
      } while (iVar10 < iVar14);
    }
    if (0 < local_30c) {
      do {
        uVar12 = RNG__Next();
        FUN_00407480();
        uVar11 = FUN_00813520(local_300,param_1 + 0xcf,0x42200000,0,0,0);
        FUN_00428b20(5,10,uVar11,&DAT_00c7b640,param_1,0xb,uVar12);
        local_30c = local_30c + -1;
      } while (local_30c != 0);
    }
    if (0 < local_2f8) {
      do {
        uVar12 = RNG__Next();
        FUN_00407480();
        uVar11 = FUN_00813520(local_374,param_1 + 0xcf,0x42200000,0,0,0);
        FUN_00428b20(5,10,uVar11,&DAT_00c7b640,param_1,4,uVar12);
        local_2f8 = local_2f8 + -1;
      } while (local_2f8 != 0);
    }
    local_298 = param_1 + 0xcf;
    piVar5 = local_298;
    piVar21 = local_298;
    if (0 < (int)local_2c8) {
      do {
        uVar12 = RNG__Next();
        FUN_00407480();
        uVar11 = FUN_00813520(local_330,param_1 + 0xcf,0x42200000,0,0,0);
        FUN_00428b20(5,10,uVar11,&DAT_00c7b640,param_1,7,uVar12);
        local_2c8 = (int *)((int)local_2c8 + -1);
      } while (local_2c8 != (int *)0x0);
      local_2ec = param_1 + 0xcf;
      local_2c8 = (int *)0x0;
      piVar5 = local_298;
      piVar21 = local_298;
    }
    while (local_2b0 = piVar21, piVar19 = local_2b0, piVar21 = local_2b0, 0 < (int)local_2a8) {
      if (local_2a8 < 100) {
        if (0x18 < local_2a8) {
          uVar12 = 0x4a;
          iVar14 = -0x19;
          goto LAB_007b5662;
        }
        local_2c4 = CONCAT44(0x14,(uint)local_2c4);
        if (local_2a8 < 10) {
          if (local_2a8 < 5) {
            if (local_2a8 < 2) {
              uVar12 = 1;
              local_2a8 = local_2a8 - 1;
            }
            else {
              uVar12 = 4;
              local_2a8 = local_2a8 - 2;
            }
          }
          else {
            uVar12 = 2;
            local_2a8 = local_2a8 - 5;
          }
        }
        else {
          uVar12 = 3;
          local_2a8 = local_2a8 - 10;
        }
        local_298 = (int *)RNG__Next();
        FUN_00407480();
        piVar5 = DAT_00baa904;
      }
      else {
        uVar12 = 0x12;
        iVar14 = -100;
LAB_007b5662:
        local_2a8 = local_2a8 + iVar14;
        local_2c4 = CONCAT44(100,(uint)local_2c4);
        local_298 = (int *)RNG__Next();
        FUN_00407480();
        piVar5 = DAT_00baa81c;
      }
      uVar11 = FUN_00813520(local_31c,local_2ec,piVar5,0,0,0);
      iVar14 = (int)local_2c4._4_4_;
      uVar12 = FUN_00428b20(5,local_2c4._4_4_,uVar11,&DAT_00c7b640,param_1,uVar12,local_298);
      local_2c4 = CONCAT44(uVar12,(uint)local_2c4);
      piVar5 = local_2ec;
      piVar21 = local_2b0;
      if (iVar14 == 100) {
        uVar12 = FUN_006eef60();
        uVar11 = FUN_00417290(local_360);
        FUN_00428b20(1000,0xf,uVar11,&DAT_00c7b640,0,0,uVar12);
        piVar5 = local_2ec;
        piVar21 = local_2b0;
      }
    }
    while (local_298 = piVar5, local_2c8 = piVar19, 0 < (int)local_2e4) {
      if (local_2e4 < (int *)0x63) {
        if (&DAT_00000009 < local_2e4) {
          uVar12 = 0x13;
          iVar14 = -10;
          goto LAB_007b57d2;
        }
        local_2c4 = CONCAT44(0x28,(uint)local_2c4);
        if (local_2e4 < (int *)0x2) {
          uVar12 = 1;
          iVar14 = -1;
        }
        else {
          uVar12 = 2;
          iVar14 = -2;
        }
        local_2e4 = (int *)((int)local_2e4 + iVar14);
        local_2b0 = (int *)RNG__Next();
        FUN_00407480();
        piVar5 = DAT_00baa904;
      }
      else {
        uVar12 = 0xbe;
        iVar14 = -99;
LAB_007b57d2:
        local_2e4 = (int *)((int)local_2e4 + iVar14);
        local_2c4 = CONCAT44(100,(uint)local_2c4);
        local_2b0 = (int *)RNG__Next();
        FUN_00407480();
        piVar5 = DAT_00baa81c;
      }
      uVar11 = FUN_00813520(local_368,local_298,piVar5,0,0,0);
      iVar14 = (int)local_2c4._4_4_;
      uVar12 = FUN_00428b20(5,local_2c4._4_4_,uVar11,&DAT_00c7b640,param_1,uVar12,local_2b0);
      local_2c4 = CONCAT44(uVar12,(uint)local_2c4);
      piVar19 = local_2c8;
      piVar21 = local_298;
      piVar5 = local_298;
      if (iVar14 == 100) {
        uVar12 = FUN_006eef60();
        uVar11 = FUN_00417290(local_398);
        FUN_00428b20(1000,0xf,uVar11,&DAT_00c7b640,0,0,uVar12);
        piVar19 = local_2c8;
        piVar21 = local_298;
        piVar5 = local_298;
      }
    }
    for (; local_2b0 = piVar21, local_2d8 != (code *)0x0; local_2d8 = local_2d8 + -1) {
      uVar12 = RNG__Next();
      FUN_00407480();
      uVar11 = FUN_00813520(local_344,local_2b0,0x42200000,0,0,0);
      FUN_00428b20(5,0x28,uVar11,&DAT_00c7b640,param_1,4,uVar12);
      piVar21 = local_2b0;
    }
    local_2d8 = (code *)0x0;
    piVar5 = local_2e8;
    piVar21 = local_2bc[1];
    if (0 < (int)local_2bc[1]) {
      do {
        uVar12 = RNG__Next();
        FUN_00407480();
        uVar11 = FUN_00813520(local_3b8,local_2c8,0x42200000,0,0,0);
        FUN_00428b20(5,0x28,uVar11,&DAT_00c7b640,param_1,7,uVar12);
        local_2bc[1] = (int *)((int)local_2bc[1] + -1);
        piVar5 = local_2e8;
        piVar21 = (int *)0x0;
      } while (local_2bc[1] != (int *)0x0);
    }
    while (local_2bc[1] = piVar21, 0 < (int)piVar5) {
      if (piVar5 < (int *)0x63) {
        local_2c4 = CONCAT44(0x1e,(uint)local_2c4);
        if (piVar5 < (int *)0x2) {
          local_2d8 = (code *)0x1;
          iVar14 = -1;
        }
        else {
          local_2d8 = (code *)0x3;
          iVar14 = -2;
        }
        piVar5 = (int *)((int)piVar5 + iVar14);
        local_2e8 = piVar5;
        local_2bc[1] = (int *)RNG__Next();
        FUN_00407480();
        piVar21 = DAT_00baa904;
      }
      else {
        local_2bc[1] = (int *)RNG__Next();
        piVar5 = (int *)((int)piVar5 - 99);
        local_2ec = DAT_00baa81c;
        local_2c4 = CONCAT44(100,(uint)local_2c4);
        local_2d8 = (code *)&DAT_00000011;
        local_2e8 = piVar5;
        FUN_00407480();
        piVar21 = local_2ec;
      }
      uVar12 = FUN_00813520(local_3a0,local_2c8,piVar21,0,0,0);
      local_2bc[1] = (int *)FUN_00428b20(5,local_2c4._4_4_,uVar12,&DAT_00c7b640,param_1,local_2d8,
                                         local_2bc[1]);
      piVar21 = local_2bc[1];
      if (local_2c4._4_4_ == (int *)0x64) {
        uVar12 = FUN_006eef60();
        uVar11 = FUN_00417290(local_358);
        FUN_00428b20(1000,0xf,uVar11,&DAT_00c7b640,0,0,uVar12);
        piVar5 = local_2e8;
        piVar21 = local_2bc[1];
      }
    }
    for (; local_29c != (int *)0x0; local_29c = (int *)((int)local_29c - 1)) {
      uVar12 = RNG__Next();
      FUN_00407480();
      uVar11 = FUN_00813520(local_2bc,local_2c8,0x42200000,0,0,0);
      FUN_00428b20(5,0x1e,uVar11,&DAT_00c7b640,param_1,2,uVar12);
    }
    iVar14 = 2;
    local_29c = (int *)0x0;
    do {
      FUN_00407480();
      FUN_00813520(local_380,local_2c8,0,0,0,0);
      FUN_00771800(local_380,0);
      iVar14 = iVar14 + -1;
    } while (iVar14 != 0);
    iVar14 = FUN_007ad440();
    uVar4 = 0;
    if (iVar14 != 0) {
      do {
        FUN_00407480();
        uVar12 = FUN_00813520(local_300,local_2c8,0,0,0,0);
        FUN_007a48f0(uVar4,uVar12);
        uVar4 = uVar4 + 1;
        uVar8 = FUN_007ad440();
      } while (uVar4 < uVar8);
    }
    if (local_2a1 != 0) {
      FUN_00424530();
      piVar5 = (int *)FUN_0042c7f0();
      FUN_00424510();
      local_8._0_1_ = 8;
      if (0 < (int)piVar5) {
joined_r0x007b5c54:
        piVar5 = (int *)((int)piVar5 + -1);
        local_29c = piVar5;
        if (-1 < (int)piVar5) {
          FUN_00424530();
          iVar14 = FUN_005cbe00(piVar5);
          if (*(char *)(iVar14 + 4) == '\0') {
            FUN_00424530();
            iVar14 = FUN_005cbe00(piVar5);
            local_2b0 = *(int **)(iVar14 + 8);
            cVar2 = FUN_007ce2a0(local_2b0,0);
            if (cVar2 != '\0') {
              FUN_0042ca00();
              piVar21 = (int *)FUN_0072fd10(local_2b0);
              if (*piVar21 != 3) {
                local_2bc[1] = param_1 + 0x5b2;
                iVar14 = 0;
                piVar21 = (int *)FUN_0042c810(local_2b0);
                piVar5 = local_29c;
                if (0 < *piVar21) {
                  do {
                    uVar4 = FUN_00417840();
                    param_1 = local_2d0;
                    piVar5 = local_29c;
                    if (2 < uVar4) break;
                    FUN_0042c850(&local_2b0);
                    iVar14 = iVar14 + 1;
                    piVar21 = (int *)FUN_0042c810(local_2b0);
                    param_1 = local_2d0;
                    piVar5 = local_29c;
                  } while (iVar14 < *piVar21);
                }
              }
            }
          }
          goto joined_r0x007b5c54;
        }
        uVar4 = 0;
        iVar14 = FUN_00417840();
        if (iVar14 != 0) {
          do {
            puVar13 = (undefined4 *)FUN_0042c810(uVar4);
            FUN_00790530(*puVar13,0,1);
            uVar4 = uVar4 + 1;
            uVar8 = FUN_00417840();
          } while (uVar4 < uVar8);
        }
      }
      local_8 = CONCAT31(local_8._1_3_,7);
      FID_conflict__Tidy();
    }
    FUN_005b19d0();
    FUN_007597e0(0xffffffff);
    FUN_004178e0();
    FUN_009a6110(1);
    local_8 = 0xffffffff;
    guard_check_icall();
    break;
  case 0x39:
    FUN_00930550(0x3c,1);
    FUN_00930390(0x3c,local_2a8,1);
    break;
  case 0x3a:
    FUN_00930550(0x3d,1);
    FUN_00930390(0x3d,local_2a8,1);
    break;
  case 0x3b:
    cVar2 = FUN_00930680(0x3e);
    if (cVar2 == '\0') {
      FUN_00456860();
      FUN_009ad210(0x2a,3,0);
    }
    iVar14 = param_1[0x7b3];
    param_1[0x7b3] = 0;
    FUN_00930550(0x3e,1);
    FUN_00930390(0x3e,local_2a8,1);
    param_1[0x7b3] = iVar14;
    local_29c = (int *)(((uint)local_2a1 - iVar14) + 2);
    if (0 < (int)local_29c) {
      do {
        iVar14 = FUN_007cae60(0);
        iVar10 = FUN_007cb060();
        if (iVar10 < iVar14) {
          param_1[0x7b3] = param_1[0x7b3] + 1;
          FUN_007588a0(2,0);
        }
        FUN_00758a70(2,0,0);
        local_29c = (int *)((int)local_29c + -1);
      } while (local_29c != (int *)0x0);
      local_29c = (int *)0x0;
    }
    break;
  case 0x3c:
    FUN_00424530();
    FUN_005cbd00(0x3c);
    uVar12 = RNG__Next();
    FUN_0074d780(uVar12);
    FUN_00424530();
    iVar14 = FUN_00740da0(0xffffffef,0xffffffff);
    if (*(int *)(iVar14 + 0x10) == 0) {
      FUN_005cbd00(0x3c);
      uVar12 = RNG__Next();
      FUN_006fe3d0(0,uVar12,param_1);
    }
    else {
      FUN_00424530();
      FUN_00428ae0(0xffffffff);
      FUN_006fd7c0(0xffffffef,0xffffffff,3,param_1,0);
    }
    goto LAB_007b8998;
  case 0x3d:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    local_29c = (int *)(local_2a1 + 2);
    do {
      uVar12 = RNG__Next();
      FUN_00407480();
      uVar11 = FUN_00813520(local_308,param_1 + 0xcf,0x42200000,0,0,0);
      FUN_00428b20(5,10,uVar11,&DAT_00c7b640,param_1,0xb,uVar12);
      local_29c = (int *)((int)local_29c + -1);
    } while (local_29c != (int *)0x0);
    local_29c = (int *)0x0;
    break;
  case 0x3e:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    local_29c = (int *)(local_2a1 + 1);
    local_2d8 = (code *)(param_1 + 0xcf);
    do {
      piVar5 = (int *)RNG__Next();
      local_2bc[1] = piVar5;
      FUN_00407480();
      uVar12 = FUN_007ec080(piVar5,0);
      FUN_00417850();
      cVar2 = FUN_00429550();
      piVar5 = local_2bc[1];
      while (cVar2 != '\0') {
        FUN_00417850();
        piVar21 = (int *)FUN_004176f0();
        cVar2 = (**(code **)(*piVar21 + 0x30))(uVar12);
        if (cVar2 == '\0') break;
        FUN_00407480();
        uVar12 = FUN_007ec080(piVar5,0);
        FUN_00417850();
        cVar2 = FUN_00429550();
      }
      FUN_00407480();
      FUN_00813520(&local_2cc,local_2d8,0x42200000,0,0,0);
      uVar11 = RNG__Next();
      FUN_00428b20(5,100,&local_2cc,&DAT_00c7b640,0,uVar12,uVar11);
      uVar12 = FUN_006eef60();
      piVar5 = (int *)FUN_00428b20(1000,0xf,&local_2cc,&DAT_00c7b640,0,0,uVar12);
      pcVar20 = *(code **)(*piVar5 + 0x3c);
      uVar12 = FUN_00435b50(0x3f800000,0x40000000,0x3ecccccd,0x3ecccccd,0x3f800000,0,0,0);
      (*pcVar20)(uVar12,0xffffffff,0xff,0,1);
      FUN_009568e0(0x13c,2,0,0x3f800000);
      param_1 = local_2d0;
      if (local_2d0[0x4d0] < 1) {
        if (local_2d0[0x762] < 1) {
          FUN_00758d00(0xfffffffc,0);
        }
        else {
          FUN_007ca840(0xffffffff);
        }
      }
      else {
        FUN_007588a0(0xfffffffe,0);
      }
      if ((param_1[0x4f0] != 10) && (param_1[0x4f0] != 0x1f)) {
        FUN_007d2a40(1);
      }
      local_29c = (int *)((int)local_29c + -1);
      param_1[0x5aa] = 0x400;
      param_1[0x5ab] = 0;
    } while (local_29c != (int *)0x0);
    local_29c = (int *)0x0;
    break;
  case 0x3f:
    cVar2 = FUN_00930680(0x3f);
    if (cVar2 == '\0') {
      FUN_006b6470(0x1e7,2,0,0x3f800000);
      FUN_00703670(4);
      local_2ec = param_1 + 0xcf;
      local_2bc[1] = (int *)0x3;
      do {
        FUN_0067f070(local_308);
        FUN_0067efe0();
        pcVar20 = (code *)((float)in_XMM0_Da * DAT_00baa784);
        local_2d8 = pcVar20;
        FUN_00a104e0(&local_2cc,&local_2d8);
        uVar12 = FUN_006eef60();
        FUN_0067f070(local_300);
        FUN_0067efe0();
        local_2c4 = CONCAT44((float)pcVar20 * DAT_00baa87c,(uint)local_2c4);
        uVar11 = FUN_00a104e0(local_374,(int)&local_2c4 + 4);
        piVar5 = local_2ec;
        uVar11 = FUN_00a10420(local_330,uVar11);
        uVar26 = 0;
        pTVar25 = &IsaacRepentancePlus::Entity_Effect::RTTI_Type_Descriptor;
        pTVar24 = &IsaacRepentancePlus::Entity::RTTI_Type_Descriptor;
        uVar7 = 0;
        uVar12 = FUN_00428b20(1000,0x3b,uVar11,&local_2cc,0,0,uVar12);
        piVar21 = (int *)__RTDynamicCast(uVar12,uVar7,pTVar24,pTVar25,uVar26);
        local_29c = DAT_00baa454;
        FUN_00417290(local_31c);
        FUN_00a10480(local_360,piVar5);
        uVar12 = FUN_00a0fe90();
        fVar22 = (float10)FUN_00a10180(uVar12);
        local_2b0 = (int *)(float)fVar22;
        piVar5 = (int *)0x0;
        if ((float)local_2b0 < 0.0) {
          local_29c = DAT_00baad50;
          piVar5 = DAT_00baad50;
        }
        FUN_0067efe0();
        fVar23 = ((float)piVar5 * (float)DAT_00baa81c + (float)DAT_00baa630) * (float)local_29c;
        FUN_00435eb0(fVar23);
        iVar14 = FUN_0067f010();
        FUN_00435e90(iVar14 + 0xf);
        uVar7 = 0;
        uVar11 = 0;
        uVar12 = 0;
        pcVar20 = *(code **)(*piVar21 + 0x3c);
        FUN_0067efe0(0,0,0);
        in_XMM0_Da = DAT_00baa454;
        uVar12 = FUN_00435ad0(fVar23 * DAT_00baa2d0 + DAT_00baa198,uVar12,uVar11,uVar7);
        (*pcVar20)(uVar12,0xffffffff,0xff,0,1);
        (**(code **)(*piVar21 + 0xc))();
        param_1 = local_2d0;
        local_2bc[1] = (int *)((int)local_2bc[1] + -1);
      } while (local_2bc[1] != (int *)0x0);
      pcVar20 = *(code **)(*local_2d0 + 0x3c);
      uVar12 = FUN_00435b50(0x3f800000,0,0,0,0,0x3f4ccccd,0x3f4ccccd,0x3f4ccccd);
      (*pcVar20)(uVar12,2,0xff,1,1);
    }
    FUN_00930550(0x3f,1);
    FUN_00930390(0x3f,1,1);
    iVar14 = RNG__RandomInt(10);
    if (iVar14 == 0) {
      FUN_0042ca00();
      uVar11 = 0;
      uVar12 = FUN_0072fda0(0x44);
      FUN_0075d1d0(uVar12,uVar11);
    }
    goto LAB_007b8998;
  case 0x40:
    iVar14 = RNG__RandomInt((local_2a1 + 1) * 3);
    piVar5 = (int *)(iVar14 + 2);
    local_29c = piVar5;
    if (piVar5 != (int *)0x0) {
      local_2bc[1] = param_1 + 0xcf;
      do {
        FUN_00407480();
        FUN_00813520(local_358,local_2bc[1],0x42200000,0,0,0);
        uVar12 = RNG__Next();
        FUN_00428b20(5,0x3c,local_358,&DAT_00c7b640,0,0,uVar12);
        piVar5 = (int *)((int)piVar5 + -1);
        param_1 = local_2d0;
      } while (piVar5 != (int *)0x0);
    }
    break;
  case 0x41:
    local_2ac = 0;
    FUN_00407480();
    FUN_00428a60();
    FUN_0041af60(local_438,5,0xffffffff,0xffffffff,0,0);
    local_8 = 9;
    piVar5 = (int *)0x0;
    local_2bc[1] = (int *)0x0;
    iVar14 = FUN_004176f0();
    if (iVar14 == 0) {
LAB_007b6afb:
      uVar11 = 0x21;
      uVar12 = RNG__Next(0x21);
      RNG__game_constructor(uVar12,uVar11);
      local_8 = CONCAT31(local_8._1_3_,0xb);
      uVar12 = RNG__Next();
      FUN_00407480();
      FUN_00407480();
      uVar11 = FUN_00812d00(local_308);
      uVar11 = FUN_00813520(local_300,uVar11,0,0,0,0);
      FUN_00428b20(5,0x14,uVar11,&DAT_00c7b640,0,1,uVar12);
      guard_check_icall();
    }
    else {
      do {
        puVar13 = (undefined4 *)FUN_00417620(piVar5);
        local_2b0 = (int *)*puVar13;
        cVar2 = FUN_00417460();
        if ((((cVar2 == '\0') || (cVar2 = FUN_00417470(), cVar2 != '\0')) ||
            (cVar2 = FUN_005b1930(), cVar2 != '\0')) ||
           (((cVar2 = FUN_00417480(), cVar2 == '\0' || (iVar14 = FUN_005b1940(), 0 < iVar14)) ||
            (cVar2 = FUN_006ee200(), cVar2 == '\0')))) goto switchD_007b66d7_caseD_b;
        uVar4 = FUN_00417270();
        if (uVar4 < 0x47) {
          if (uVar4 == 0x46) {
LAB_007b6844:
            local_2a8 = 5;
          }
          else {
            switch(uVar4) {
            case 10:
              iVar14 = FUN_00417280();
              if ((iVar14 == 4) || (iVar14 = FUN_00417280(), iVar14 == 7)) {
LAB_007b6706:
                local_2a8 = 10;
              }
              else {
                iVar14 = FUN_00417280();
                if (((iVar14 == 6) || (iVar14 = FUN_00417280(), iVar14 == 0xb)) ||
                   (iVar14 = FUN_00417280(), iVar14 == 5)) {
                  local_2a8 = 6;
                }
                else {
                  iVar14 = FUN_00417280();
                  if (iVar14 == 3) goto LAB_007b6844;
                  iVar14 = FUN_00417280();
                  if ((iVar14 == 8) || (iVar14 = FUN_00417280(), iVar14 == 0xc)) {
                    local_2a8 = 2;
                  }
                  else {
                    iVar14 = FUN_00417280();
                    local_2a8 = (uint)(iVar14 != 2) * 2 + 1;
                  }
                }
              }
              break;
            default:
              goto switchD_007b66d7_caseD_b;
            case 0x1e:
              iVar14 = FUN_00417280();
              if (((iVar14 == 3) || (iVar14 = FUN_00417280(), iVar14 == 2)) ||
                 (iVar14 = FUN_00417280(), iVar14 == 4)) goto LAB_007b6706;
              goto LAB_007b6844;
            case 0x28:
              iVar14 = FUN_00417280();
              if ((iVar14 == 2) || (iVar14 = FUN_00417280(), iVar14 == 4)) goto LAB_007b6706;
              iVar14 = FUN_00417280();
              if (iVar14 != 7) goto LAB_007b6844;
              local_2a8 = 10;
              break;
            case 0x45:
              local_2a8 = 7;
            }
          }
LAB_007b684f:
          uVar11 = 0x10;
          uVar12 = FUN_00505b70(0x10);
          RNG__game_constructor(uVar12,uVar11);
          local_8 = CONCAT31(local_8._1_3_,10);
          if (9 < local_2a8) {
            local_29c = (int *)((local_2a8 - 5) / 5);
            local_2a8 = local_2a8 + (int)local_29c * -5;
            do {
              uVar12 = RNG__Next();
              RNG__Next();
              uVar11 = FUN_0067f0d0();
              fVar22 = (float10)RNG__RandomFloat();
              local_2d8 = (code *)(float)fVar22;
              FUN_004171d0(uVar11);
              local_2c4 = CONCAT44(0x40a00000,(uint)local_2c4);
              uVar11 = FUN_00a104e0(local_374,(int)&local_2c4 + 4);
              uVar7 = FUN_00417290(local_330);
              FUN_00428b20(5,0x14,uVar7,uVar11,0,2,uVar12);
              local_29c = (int *)((int)local_29c - 1);
            } while (local_29c != (int *)0x0);
            local_29c = (int *)0x0;
          }
          if (0 < (int)local_2a8) {
            do {
              uVar12 = RNG__Next();
              RNG__Next();
              uVar11 = FUN_0067f0d0();
              fVar22 = (float10)RNG__RandomFloat();
              local_2ec = (int *)(float)fVar22;
              FUN_004171d0(uVar11);
              local_2c8 = (int *)0x40a00000;
              uVar11 = FUN_00a104e0(local_368,&local_2c8);
              uVar7 = FUN_00417290(local_398);
              FUN_00428b20(5,0x14,uVar7,uVar11,0,1,uVar12);
              local_2a8 = local_2a8 - 1;
            } while (local_2a8 != 0);
          }
          uVar12 = FUN_006eef60();
          uVar11 = FUN_00417290(local_344);
          piVar5 = (int *)FUN_00428b20(1000,0xf,uVar11,&DAT_00c7b640,0,0,uVar12);
          pcVar20 = *(code **)(*piVar5 + 0x3c);
          uVar12 = FUN_00435b50(0x3f800000,0x40400000,0x4019999a,0x3f800000,0x3f800000,0,0,0);
          (*pcVar20)(uVar12,0xffffffff,0xff,0,1);
          piVar5 = local_2b0;
          cVar2 = FUN_00417220(5,100,0xffffffff);
          if (cVar2 == '\0') {
            (**(code **)(*piVar5 + 0x28))();
          }
          else {
            FUN_0060d1f0(4);
          }
          FUN_006ee750();
          uVar4 = local_2ac + 1;
          local_8 = CONCAT31(local_8._1_3_,9);
          local_2ac = uVar4;
          guard_check_icall();
        }
        else {
          if (300 < uVar4) {
            if (uVar4 != 0x15e) goto switchD_007b66d7_caseD_b;
            goto LAB_007b6844;
          }
          if ((uVar4 == 300) || (uVar4 == 0x5a)) goto LAB_007b6844;
          if (uVar4 == 100) {
            iVar14 = FUN_00417280();
            local_2a8 = -(uint)(iVar14 != 0) & 0xf;
            if (local_2a8 != 0) goto LAB_007b684f;
          }
switchD_007b66d7_caseD_b:
          uVar4 = local_2ac;
          local_2bc[1] = piVar5;
        }
        piVar5 = (int *)((int)local_2bc[1] + 1);
        local_2bc[1] = piVar5;
        piVar21 = (int *)FUN_004176f0();
      } while (piVar5 < piVar21);
      if (uVar4 == 0) goto LAB_007b6afb;
      RNG__Next();
    }
    local_8 = 0xffffffff;
    FUN_004175b0();
    param_1 = local_2d0;
    break;
  case 0x42:
    FUN_00440ee0(0x3f800000,0x3c);
    FUN_00703670(0x32);
    local_29c = (int *)RNG__RandomInt(6);
    local_2bc[1] = (int *)RNG__Next();
    piVar5 = local_29c;
    if (local_29c == (int *)0x0) {
      FUN_005b39d0((int)&local_2e8 + 2,0x11c,0x11,0xffffffff,0);
    }
    else {
      if ((((local_29c == (int *)0x1) || (local_29c == (int *)&DAT_00000005)) ||
          (local_29c == (int *)0x2)) &&
         ((FUN_005b39d0((int)&local_2e4 + 2,0xa6,1,0xffffffff,0), piVar5 == (int *)0x2 ||
          (piVar5 == (int *)&DAT_00000005)))) {
        FUN_00704c50(local_2bc[1]);
      }
      if ((piVar5 == (int *)0x3) || (piVar5 == (int *)&DAT_00000005)) {
        FUN_00704b70();
        FUN_005b39d0((int)&local_2f4 + 2,0x69,1,0xffffffff,0);
      }
      if (piVar5 == (int *)&DAT_00000004) {
        FUN_0042a340();
        FUN_00424530();
        uVar12 = FUN_004360f0();
        Seeds__advance_stage_slot(uVar12);
        FUN_006fdc10(1,0,0);
      }
      else if (piVar5 == (int *)&DAT_00000005) {
        uVar4 = 0;
        iVar14 = FUN_004178d0();
        if (iVar14 != 0) {
          do {
            local_29c = (int *)PlayerManager__get_player_417870(uVar4);
            iVar14 = FUN_00417270();
            if (iVar14 == 0) {
              FUN_005b39d0((int)&local_310 + 2,0x11c,0x11,0xffffffff,0);
            }
            uVar4 = uVar4 + 1;
            uVar8 = FUN_004178d0();
          } while (uVar4 < uVar8);
        }
      }
    }
    break;
  case 0x43:
    FUN_00407480();
    FUN_004360d0();
    FUN_00930390(0x40,1,1);
    break;
  case 0x44:
    FUN_00930390(0x41,1,1);
    break;
  case 0x45:
    FUN_005b39d0((int)&local_2ac + 2,0x221,3,0xffffffff,0);
    break;
  case 0x46:
    if ((char)local_2ac != '\0') {
      ExceptionList = local_10;
      return;
    }
    iVar14 = 5;
    if (local_2a1 != 0) {
      iVar14 = 10;
    }
    do {
      FUN_00930390(0x45,1,1);
      iVar14 = iVar14 + -1;
      param_1 = local_2d0;
    } while (iVar14 != 0);
    goto LAB_007b8998;
  case 0x47:
    cVar2 = FUN_00930680(0x43);
    if (cVar2 == '\0') {
      FUN_006b6470(0x10a,2,0,0x3f800000);
      FUN_00456860();
      FUN_009ad210(10,3,0);
    }
    FUN_00930550(0x43,1);
    FUN_00930390(0x43,1,1);
    FUN_005b39d0((int)&local_2a8 + 2,0x21,3,0xffffffff,0);
    break;
  case 0x48:
    uVar11 = 0x2d;
    uVar12 = RNG__Next(0x2d);
    RNG__game_constructor(uVar12,uVar11);
    local_8 = 0xc;
    memset(local_1d4,0,0x1c0);
    local_298 = (int *)FUN_00407480();
    uVar4 = FUN_004176f0();
    local_2a8 = uVar4;
    local_2ac = FUN_0040c2e0();
    local_2c8 = (int *)(local_2ac * uVar4);
    FUN_00428a60();
    FUN_0041af60(local_3c8,1000,0xa1,0xffffffff,0,0);
    local_8 = CONCAT31(local_8._1_3_,0xd);
    if (0 < (int)local_2c8) {
      iVar14 = 0;
      do {
        uVar11 = 0;
        uVar12 = FUN_00812f00(local_308,iVar14);
        cVar2 = FUN_00813360(uVar12,uVar11);
        if (cVar2 != '\0') {
          local_29c = (int *)FUN_00436060(iVar14);
          iVar10 = FUN_007f0800(iVar14);
          if (iVar10 == 0) {
            if (local_29c != (int *)0x0) {
              FUN_004073c0();
              cVar2 = FUN_0070bf80();
              if (cVar2 != '\0') goto LAB_007b6f0b;
            }
            local_2b0 = (int *)0x0;
            iVar10 = FUN_004176f0();
            if (iVar10 != 0) {
              do {
                FUN_00417620(local_2b0);
                uVar12 = FUN_00417290(local_300);
                iVar10 = FUN_00812c90(uVar12);
                if (iVar10 == iVar14) goto LAB_007b6f0b;
                local_2b0 = (int *)((int)local_2b0 + 1);
                piVar5 = (int *)FUN_004176f0();
              } while (local_2b0 < piVar5);
            }
            local_1d4[iVar14] = '\x05';
          }
        }
LAB_007b6f0b:
        iVar14 = iVar14 + 1;
        uVar4 = local_2a8;
        param_1 = local_2d0;
      } while (iVar14 < (int)local_2c8);
    }
    local_2f4 = (int *)(uVar4 - 1);
    local_29c = (int *)0x1;
    if (1 < (int)local_2f4) {
      iVar14 = uVar4 - 1;
      local_2c4 = CONCAT44(local_2ac - 1,(uint)local_2c4);
      do {
        if (1 < (int)(local_2ac - 1)) {
          pcVar18 = local_1d4 + (int)local_29c;
          pcVar9 = (char *)((int)local_29c + (int)(local_1d4 + uVar4 * 2));
          local_2d8 = (code *)(-1 - uVar4);
          pcVar15 = pcVar18 + uVar4;
          local_2bc[1] = (int *)(1 - uVar4);
          iVar14 = local_2ac - 2;
          do {
            if ((((*pcVar15 != '\0') &&
                 (uVar4 = local_2a8, *(char *)((int)local_2bc[1] + (int)pcVar9) != '\0')) &&
                (local_2d8[(int)pcVar9] != (code)0x0)) && ((*pcVar9 != '\0' && (*pcVar18 != '\0'))))
            {
              *pcVar15 = '2';
            }
            pcVar9 = pcVar9 + uVar4;
            pcVar18 = pcVar18 + uVar4;
            pcVar15 = pcVar15 + uVar4;
            iVar14 = iVar14 + -1;
          } while (iVar14 != 0);
          iVar14 = uVar4 - 1;
        }
        local_29c = (int *)((int)local_29c + 1);
        param_1 = local_2d0;
      } while ((int)local_29c < iVar14);
    }
    local_2b0 = (int *)0x0;
    do {
      FUN_00424510();
      piVar5 = local_2c8;
      iVar14 = 0;
      local_8 = CONCAT31(local_8._1_3_,0xe);
      bVar1 = false;
      if ((int)local_2c8 < 1) {
LAB_007b73c1:
        thunk_FUN_00426980();
        break;
      }
      do {
        if (local_1d4[iVar14] != '\0') {
          FUN_0049cb60(iVar14,(int)local_1d4[iVar14],0);
          bVar1 = true;
        }
        iVar14 = iVar14 + 1;
      } while (iVar14 < (int)piVar5);
      param_1 = local_2d0;
      if (!bVar1) goto LAB_007b73c1;
      iVar14 = FUN_0049cbf0(local_21c,uStack_218,uStack_214,uStack_210);
      FUN_00812f00(local_308,iVar14);
      fVar22 = (float10)RNG__RandomFloat();
      local_29c = (int *)(float)(fVar22 * (float10)DAT_00baa8f0 - (float10)DAT_00baa868);
      fVar22 = (float10)RNG__RandomFloat();
      local_2bc[1] = (int *)(float)(fVar22 * (float10)DAT_00baa8f0 - (float10)DAT_00baa868);
      uVar12 = FUN_00a0fe90();
      FUN_00a10420(local_314,uVar12);
      local_2bc[1] = (int *)0x0;
      iVar10 = iVar14 % (int)local_2a8;
      local_2c4 = CONCAT44(iVar14 / (int)local_2a8,(uint)local_2c4);
      local_29c = (int *)(iVar10 + -2);
      puVar13 = (undefined4 *)FUN_0041cb80();
      pcVar20 = (code *)*puVar13;
      local_2e4 = (int *)(iVar10 + 2);
      local_2bc[1] = local_2f4;
      local_2d8 = pcVar20;
      local_29c = local_2e4;
      piVar5 = (int *)FUN_0041cb60();
      if ((int)pcVar20 <= *piVar5) {
        local_2e8 = (int *)((int)local_2c4._4_4_ - 2);
        piVar5 = (int *)((int)local_2c4._4_4_ + 2);
        local_2ec = piVar5;
        do {
          local_2bc[1] = (int *)0x0;
          local_29c = local_2e8;
          piVar21 = (int *)FUN_0041cb80();
          iVar14 = *piVar21;
          local_2bc[1] = (int *)(local_2ac - 1);
          local_2c4 = CONCAT44(iVar14,(uint)local_2c4);
          local_29c = piVar5;
          piVar21 = (int *)FUN_0041cb60();
          if (iVar14 <= *piVar21) {
            pcVar20 = local_2d8 + iVar14 * local_2a8;
            do {
              if (local_1d4[(int)pcVar20] != '\0') {
                FUN_00812f00(local_358,pcVar20);
                fVar22 = (float10)FUN_00a0ff90(local_314);
                local_29c = (int *)(float)fVar22;
                if (DAT_00baac20 < (float)local_29c) {
                  local_1d4[(int)pcVar20] = '\x01';
                }
                else {
                  if ((code *)0x1bf < pcVar20) {
                    /* WARNING: Subroutine does not return */
                    FUN_00aef86f();
                  }
                  local_1d4[(int)pcVar20] = '\0';
                  uVar12 = RNG__Next();
                  FUN_00407480();
                  uVar11 = FUN_00812f00(local_374,pcVar20);
                  piVar5 = (int *)FUN_00428b20(1000,0xb1,uVar11,&DAT_00c7b640,local_2d0,1,uVar12);
                  FUN_00435e90(local_2b0);
                  (**(code **)(*piVar5 + 0xc))();
                  iVar14 = (int)local_2c4._4_4_;
                }
              }
              pcVar20 = pcVar20 + local_2a8;
              local_29c = local_2ec;
              iVar14 = iVar14 + 1;
              local_2bc[1] = (int *)(local_2ac - 1);
              local_2c4 = CONCAT44(iVar14,(uint)local_2c4);
              piVar21 = (int *)FUN_0041cb60();
              piVar5 = local_2ec;
            } while (iVar14 <= *piVar21);
          }
          local_29c = local_2e4;
          pcVar20 = local_2d8 + 1;
          local_2bc[1] = local_2f4;
          local_2d8 = pcVar20;
          piVar21 = (int *)FUN_0041cb60();
        } while ((int)pcVar20 <= *piVar21);
      }
      uVar12 = RNG__Next();
      param_1 = local_2d0;
      piVar5 = (int *)FUN_00428b20(1000,0xb1,local_314,&DAT_00c7b640,local_2d0,0,uVar12);
      FUN_00435e90(local_2b0);
      (**(code **)(*piVar5 + 0xc))();
      thunk_FUN_00426980();
      local_2b0 = (int *)((int)local_2b0 + 5);
    } while ((int)local_2b0 < 0x23);
    FUN_004175b0();
    local_8 = 0xffffffff;
    guard_check_icall();
    break;
  case 0x49:
    FUN_00424530();
    local_2bc[1] = (int *)FUN_0042c7f0();
    if (0 < (int)local_2bc[1]) {
      iVar14 = 0;
      do {
        FUN_00424530();
        piVar5 = (int *)FUN_005cbe00(iVar14);
        if (((char)piVar5[1] == '\0') && (0 < *piVar5)) {
          FUN_00424530();
          iVar10 = FUN_005cbe00(iVar14);
          local_29c = *(int **)(iVar10 + 8);
          cVar2 = FUN_007ce2a0(local_29c,0);
          if (cVar2 != '\0') {
            FUN_0042ca00();
            piVar5 = (int *)FUN_0072fd10(local_29c);
            if ((*piVar5 != 3) && (piVar5 = (int *)FUN_0042c810(local_29c), 0 < *piVar5)) {
              FUN_0078fec0(iVar14,1);
              FUN_007ab380(local_29c,"Pickup","PlayerPickupSparkle");
              FUN_00930550(0x46,1);
              FUN_00930390(0x46,1,1);
              goto LAB_007b8998;
            }
          }
        }
        iVar14 = iVar14 + 1;
      } while (iVar14 < (int)local_2bc[1]);
    }
    break;
  case 0x4a:
    FUN_00424530();
    uVar11 = 1;
    uVar12 = 0x1d;
LAB_007b34ad:
    iVar14 = FUN_007484c0(uVar12,0,piVar5,uVar11);
    if (-1 < iVar14) {
      FUN_00424530();
      FUN_00428ae0(0xffffffff);
      FUN_006fd7c0(iVar14,0xffffffff,3,param_1,0xffffffff);
      goto LAB_007b8998;
    }
    break;
  case 0x4b:
    cVar2 = FUN_00930680(0x42);
    if (cVar2 == '\0') {
      FUN_00456860();
      FUN_009ad210(0x2b,0,0);
    }
    FUN_00930550(0x42,1);
    FUN_00930390(0x42,1,1);
    if ((0 < param_1[0x4d0]) && (iVar14 = FUN_007cafe0(), iVar14 == 0)) {
      FUN_00417850();
      cVar2 = FUN_00429550();
      if (cVar2 == '\0') {
        iVar14 = param_1[0x4d0];
        param_1[0x4d0] = 0;
        iVar14 = iVar14 / 2;
        param_1[0x762] = param_1[0x762] + iVar14;
        param_1[0x763] = param_1[0x763] << ((byte)iVar14 & 0x1f) | (1 << ((byte)iVar14 & 0x1f)) - 1U
        ;
        FUN_007c9ea0();
        param_1[0x7b5] = iVar14;
        break;
      }
    }
    FUN_00417850();
    cVar2 = FUN_00429550();
    if (cVar2 != '\0') {
      param_1[0x762] = param_1[0x762] + param_1[0x4d1];
      param_1[0x4d0] = 0;
      param_1[0x4d1] = 0;
    }
    break;
  case 0x4c:
    FUN_006b6470(0x109,2,0,0x3f800000);
    uVar12 = RNG__Next();
    FUN_00407480();
    uVar11 = FUN_00813520(local_308,param_1 + 0xcf,0x42200000,0,0,0);
    piVar5 = (int *)0xa;
LAB_007b31f0:
    FUN_00428b20(6,piVar5,uVar11,&DAT_00c7b640,0,0,uVar12);
    FUN_004173e0(4,0);
    break;
  case 0x4d:
    FUN_00407480();
    local_29c = (int *)FUN_00812c90(param_1 + 0xcf);
    if (-1 < (int)local_29c) {
      FUN_00407480();
      uVar12 = FUN_006eef60();
      FUN_007ebca0(local_29c,0x12,0,uVar12,0);
      FUN_00407480();
      local_29c = (int *)FUN_00436060(local_29c);
      if (((local_29c != (int *)0x0) && (iVar14 = FUN_004073c0(), iVar14 == 0x12)) &&
         (iVar14 = FUN_0043eec0(), iVar14 == 0)) {
        FUN_00424530();
        FUN_00428a80(0xd,1);
        uVar12 = FUN_006eef60();
        uVar11 = FUN_00709df0(local_308);
        piVar5 = (int *)FUN_00428b20(1000,0xf,uVar11,&DAT_00c7b640,0,0,uVar12);
        (**(code **)(*piVar5 + 0xc))();
      }
    }
    break;
  case 0x4e:
    FUN_005b39d0((int)&local_298 + 2,0x244,1,0xffffffff,0);
    break;
  case 0x4f:
    iVar14 = RNG__RandomInt(0x14);
    local_2bc[1] = (int *)(iVar14 + 1);
    local_29c = (int *)0x0;
    if (local_2bc[1] != (int *)0x0) {
      do {
        uVar12 = RNG__Next();
        FUN_00407480();
        uVar11 = FUN_00813520(local_308,param_1 + 0xcf,0x42200000,0,0,0);
        piVar5 = (int *)FUN_00428b20(5,10,uVar11,&DAT_00c7b640,param_1,1,uVar12);
        FUN_005b19f0(local_29c);
        (**(code **)(*piVar5 + 0xc))();
        local_29c = (int *)((int)local_29c + 1);
      } while (local_29c < local_2bc[1]);
    }
    break;
  case 0x50:
    if (-1 < (char)(byte)param_3) {
      cVar2 = (char)param_1[0x824];
      if (cVar2 == '\x01') {
        FUN_007b2230(param_1[0x825],0x180);
      }
      else if (cVar2 == '\0') {
        FUN_007c4180(param_1[0x825],param_1[0x826],0x180);
        if (param_1[0x55d] != 0) {
          FUN_007584b0();
          FUN_00763570();
        }
      }
      else if (cVar2 == '\x02') {
        FUN_005b39d0((int)&local_298 + 2,param_1[0x825],0x484,0xffffffff,param_1[0x826]);
        FUN_005ca470(param_1[0x825],0);
        goto LAB_007b8998;
      }
    }
    break;
  case 0x51:
    FUN_00407480();
    FUN_00428a60();
    FUN_0041af60(&local_20c,5,100,0xffffffff,0,0);
    local_8 = 0xf;
    piVar5 = (int *)0x0;
    local_29c = (int *)0x0;
    iVar14 = FUN_004176f0();
    if (iVar14 != 0) {
      do {
        FUN_00417620(piVar5);
        cVar2 = FUN_00417470();
        if ((((cVar2 == '\0') && (iVar14 = FUN_00417280(), iVar14 != 0)) &&
            ((local_2bc[1] = (int *)FUN_00435e30(), local_2bc[1] != (int *)0x0 &&
             ((iVar14 = FUN_005b1980(), iVar14 == 0 || (iVar14 = FUN_005b1940(), iVar14 < 0)))))) &&
           (cVar2 = FUN_006ee200(), cVar2 != '\0')) {
          FUN_00407480();
          uVar12 = RNG__Next();
          uVar12 = FUN_007ec080(uVar12,0);
          FUN_006daca0(uVar12);
          uVar12 = FUN_006eef60();
          uVar11 = FUN_00417290(local_308);
          piVar5 = (int *)FUN_00428b20(1000,0xf,uVar11,&DAT_00c7b640,0,0,uVar12);
          (**(code **)(*piVar5 + 0xc))();
        }
        local_29c = (int *)((int)local_29c + 1);
        piVar21 = (int *)FUN_004176f0();
        piVar5 = local_29c;
        param_1 = local_2d0;
      } while (local_29c < piVar21);
    }
    local_8 = 0xffffffff;
    FUN_004175b0();
    break;
  case 0x52:
    FUN_00930390(0x72,1,1);
    break;
  case 0x53:
    FUN_009568e0(0xcc,2,0,0x3f800000);
    local_2b0 = (int *)0x0;
    do {
      FUN_00424530();
      FUN_00424530();
      uVar12 = FUN_004360e0();
      cVar2 = FUN_0074cd70(uVar12,local_2b0);
      if (cVar2 != '\0') {
        FUN_00424530();
        FUN_00424530();
        uVar12 = FUN_004360e0();
        FUN_0074d010(uVar12,local_2b0);
      }
      FUN_00407480();
      piVar5 = local_2b0;
      local_29c = (int *)FUN_00436020(local_2b0);
      if (((local_29c != (int *)0x0) && (cVar2 = FUN_0056ff60(0x10), cVar2 == '\0')) &&
         (cVar2 = FUN_00710480(param_1,1), cVar2 == '\0')) {
        FUN_00710dd0();
        FUN_0070fb60(0,0);
      }
      local_2b0 = (int *)((int)piVar5 + 1);
    } while ((int)local_2b0 < 8);
    FUN_00407480();
    FUN_004360d0();
    FUN_009302e0(0xaf,1,1);
    break;
  case 0x54:
    FUN_0042ca00();
    uVar12 = FUN_0072fd10(0x2c1);
    FUN_00435f80(uVar12);
    local_458 = 0x5a - local_458;
    FUN_00930220(local_460,1,1);
    FUN_00930390(0x80,1,1);
    FUN_00407480();
    FUN_007ea260(0x5a);
    FUN_005b39d0((int)&local_2d0 + 2,0x2c1,9,0xffffffff,0);
    break;
  case 0x55:
    FUN_00930390(0x73,1,1);
    FUN_006b6470(0x25,2,0,0x3f800000);
    FUN_006b6470(0x95,2,0,0x3fc00000);
    uVar12 = FUN_006eef60();
    piVar5 = (int *)FUN_00428b20(1000,0xc3,param_1 + 0xcf,&DAT_00c7b640,param_1,1,uVar12);
    FUN_00435e90(0x24);
    FUN_006a92a0(param_1);
    (**(code **)(*piVar5 + 0xc))();
    break;
  case 0x56:
    local_29c = (int *)&DAT_0000000f;
    do {
      FUN_00407480();
      FUN_0043eed0(local_2bc + 2);
      FUN_00407480();
      FUN_0067efe0();
      local_2d8 = (code *)(DAT_00baae4c - (float)in_XMM0_Da * DAT_00baaa00);
      FUN_0067f070(local_308);
      local_2bc[1] = (int *)0x447a0000;
      uVar12 = FUN_00a104e0(local_300,local_2bc + 1);
      uVar12 = FUN_00a10420(local_374,uVar12);
      uVar12 = FUN_00436090(local_330,uVar12,local_2d8);
      FUN_007dd3b0(uVar12);
      uVar12 = FUN_006eef60();
      piVar5 = (int *)FUN_00428b20(1000,0xc5,local_2bc + 2,&DAT_00c7b640,param_1,0,uVar12);
      local_2d8 = *(code **)(*piVar5 + 0x40);
      cVar2 = FUN_007706e0(0xf7,0);
      in_XMM0_Da = DAT_00baa454;
      if (cVar2 != '\0') {
        in_XMM0_Da = DAT_00baa630;
      }
      (*local_2d8)(in_XMM0_Da);
      iVar14 = FUN_0067f010();
      FUN_00435e90(iVar14 + 300);
      uVar12 = FUN_0067f010();
      FUN_00435e60(uVar12);
      (**(code **)(*piVar5 + 0xc))();
      local_29c = (int *)((int)local_29c + -1);
    } while (local_29c != (int *)0x0);
    break;
  case 0x57:
    FUN_0042ca00();
    uVar12 = FUN_0072fd10(0x2c0);
    FUN_00435f80(uVar12);
    local_388 = 300;
    FUN_00930220(local_390,1,1);
    FUN_006b6470(0x250,2,0,0x3f800000);
    FUN_006b6470(0x28a,2,0,0x3f800000);
    FUN_00407480();
    FUN_007eb870();
    break;
  case 0x58:
    FUN_00417850();
    cVar2 = FUN_00429550();
    iVar14 = 0xf0;
    if (cVar2 != '\0') {
      iVar14 = 0x5a;
    }
    param_1[0x63d] = iVar14;
    FUN_0042ca00();
    uVar11 = 0;
    uVar12 = FUN_0072fda0(0x1f);
    FUN_0075d1d0(uVar12,uVar11);
    break;
  case 0x59:
    FUN_00930550(0x71,0xffffffff);
    FUN_00930390(0x71,1,1);
    pcVar20 = *(code **)(*param_1 + 0x24);
    uVar12 = FUN_00435c70();
    (*pcVar20)(uVar12);
    param_1[0x5aa] = 0;
    param_1[0x5ab] = 0;
    param_1[0x59f] = 0;
    param_1[0x5a0] = 0;
    goto LAB_007b8998;
  case 0x5a:
    FUN_00407480();
    FUN_004360d0();
    FUN_009302e0(0x192,1,1);
    FUN_005b39d0((int)&local_2d0 + 2,0x69,1,0xffffffff,0);
    FUN_005b39d0((int)&local_298 + 2,0xa6,1,0xffffffff,0);
    FUN_00407480();
    FUN_004360d0();
    FUN_009304a0(0x192,0xffffffff);
    break;
  case 0x5b:
    FUN_007d87a0();
    FUN_00930550(0x70,0xffffffff);
    FUN_00930390(0x70,1,2);
    iVar14 = FUN_004253b0();
    if (iVar14 != 10) {
      FUN_009302e0(0x139,1,1);
      FUN_0040c340("Shimmer");
      local_8 = 0x10;
      FUN_00759f50(0x139,1,&uStack_244,0xffffffff,0);
      local_8 = 0xffffffff;
      thunk_FUN_0040d040();
    }
    break;
  case 0x5c:
    FUN_00424510();
    local_8 = 0x11;
    FUN_0042a330();
    iVar14 = FUN_00732c70(0x1c);
    local_2b0 = (int *)(iVar14 + 4);
    local_2c8 = (int *)0x0;
    iVar14 = FUN_00414410();
    if (iVar14 != 0) {
      do {
        iVar14 = FUN_004143f0(local_2c8);
        if (*(char *)(iVar14 + 0x14) != '\0') {
          FUN_00417850();
          cVar2 = FUN_00429550();
          if (cVar2 != '\0') {
            FUN_00417850();
            piVar5 = (int *)FUN_004176f0();
            pcVar20 = *(code **)(*piVar5 + 0x30);
            puVar13 = (undefined4 *)FUN_004143f0(local_2c8);
            cVar2 = (*pcVar20)(*puVar13);
            if (cVar2 != '\0') goto LAB_007b81fb;
          }
          FUN_0042ca00();
          puVar13 = (undefined4 *)FUN_004143f0(local_2c8);
          piVar5 = (int *)FUN_0072fd10(*puVar13);
          if ((piVar5 != (int *)0x0) && (*piVar5 == 4)) {
            cVar2 = FUN_005b1500(0x8000000,0);
            if ((cVar2 == '\0') || (cVar2 = FUN_007706e0(piVar5[1],0), cVar2 == '\0')) {
              FUN_0042c850(piVar5 + 1);
            }
          }
        }
LAB_007b81fb:
        piVar21 = (int *)((int)local_2c8 + 1);
        local_2c8 = piVar21;
        piVar5 = (int *)FUN_00414410();
        param_1 = local_2d0;
      } while (piVar21 < piVar5);
    }
    cVar2 = FUN_004bc660();
    if (cVar2 == '\0') {
      uVar12 = FUN_00417840();
      uVar12 = RNG__RandomInt(uVar12);
      puVar13 = (undefined4 *)FUN_0042c810(uVar12);
      piVar5 = (int *)*puVar13;
      local_29c = piVar5;
      FUN_0042ca00();
      uVar12 = FUN_0072fd10(piVar5);
      if ((param_3 & 0x800) == 0) {
        FUN_004178e0();
        FUN_009a2d20(param_1,uVar12);
      }
      FUN_009568e0(0x80,2,0,0x3f800000);
      FUN_007ab380(local_29c,"Pickup","PlayerPickupSparkle");
      FUN_0075e050(uVar12,0xffffffff,0,0,0xffffffff);
      local_2de = 0;
    }
    local_8 = 0xffffffff;
    FID_conflict__Tidy();
    break;
  case 0x5d:
    iVar14 = RNG__RandomInt(0x19);
    local_2bc[1] = (int *)(iVar14 + 1);
    local_29c = (int *)0x0;
    if (local_2bc[1] != (int *)0x0) {
      do {
        uVar12 = RNG__Next();
        FUN_00407480();
        uVar11 = FUN_00813520(local_308,param_1 + 0xcf,0x42200000,0,0,0);
        piVar5 = (int *)FUN_00428b20(5,0x14,uVar11,&DAT_00c7b640,param_1,0,uVar12);
        FUN_005b19f0(local_29c);
        (**(code **)(*piVar5 + 0xc))();
        local_29c = (int *)((int)local_29c + 1);
      } while (local_29c < local_2bc[1]);
    }
    break;
  case 0x5e:
    local_29c = (int *)0x0;
    FUN_00417850();
    FUN_00429550();
    local_2bc[1] = param_1 + 0xcf;
    do {
      uVar12 = FUN_006eef60();
      iVar14 = RNG__RandomInt(5);
      uVar11 = FUN_0067f070(local_308);
      uVar11 = FUN_00a10420(local_300,uVar11);
      param_1 = local_2d0;
      piVar5 = (int *)FUN_00428b20(3,0x2b,uVar11,&DAT_00c7b640,local_2d0,iVar14 + 1,uVar12);
      (**(code **)(*piVar5 + 0xc))();
      piVar5 = (int *)((int)local_29c + 1);
      local_29c = piVar5;
      FUN_00417850();
      cVar2 = FUN_00429550();
      iVar14 = 0xf;
      if (cVar2 != '\0') {
        iVar14 = 10;
      }
    } while ((int)piVar5 < iVar14);
    break;
  case 0x5f:
    FUN_00417860();
    local_29c = (int *)FUN_009b9cd0(0x10);
    FUN_007a6450(param_1[0x586],0);
    FUN_006a92a0(param_1);
    uVar12 = FUN_00a0fe90();
    uVar12 = FUN_00a10420(local_300,uVar12);
    FUN_004288f0(uVar12);
    FUN_004361c0();
    FUN_00930390(0x78,1,1);
    FUN_007cbcd0();
    FUN_007bc740();
    FUN_007ca840(1);
    FUN_00758a70(2,1,0);
    uVar12 = FUN_006eef60();
    puVar16 = local_440;
    goto LAB_007b850e;
  case 0x60:
    local_29c = (int *)&DAT_00000006;
    do {
      FUN_005cbd00(0x2ad);
      FUN_0042ca00();
      FUN_00424530();
      iVar14 = FUN_00417840();
      iVar14 = RNG__RandomInt(iVar14 + -1);
      local_2bc[1] = (int *)(iVar14 + 1);
      FUN_0042ca00();
      piVar5 = (int *)FUN_0072fd10((int *)(iVar14 + 1));
      if (((piVar5 == (int *)0x0) || (cVar2 = FUN_0072fe30(local_2bc[1]), cVar2 == '\0')) ||
         (*piVar5 != 3)) {
        FUN_0042ca00();
        piVar5 = (int *)FUN_0072fd10(0x248);
      }
      if ((piVar5[0x33] == 0) || (*(short *)(piVar5[0x33] + 400) < 1)) {
        FUN_0042ca00();
        piVar5 = (int *)FUN_0072fd10(0x248);
      }
      FUN_005c93b0(piVar5[1],param_1 + 0xcf,1,0);
      local_29c = (int *)((int)local_29c + -1);
    } while (local_29c != (int *)0x0);
    FUN_00956940(0x1d7,param_1 + 0xcf,2,0,0x3f800000);
    break;
  case 0x61:
    FUN_00417860();
    piVar5 = (int *)FUN_009b9cd0(0x14);
    local_29c = piVar5;
    FUN_007a6450(param_1[0x586],0);
    FUN_006a92a0(param_1);
    uVar12 = FUN_00a0fe90();
    uVar12 = FUN_00a10420(local_308,uVar12);
    FUN_004288f0(uVar12);
    FUN_004361c0();
    FUN_00930390(0x79,1,1);
    FUN_007cbcd0();
    FUN_007bc740();
    uVar12 = FUN_005cbd00(0x2bf);
    local_2c8 = piVar5 + 0x77b;
    local_2c4 = CONCAT44(uVar12,(uint)local_2c4);
    FUN_005b16f0(1);
    local_2d8 = (code *)FUN_00424530();
    FUN_004561a0(&local_298);
    uVar12 = FUN_00456190(&local_2ec);
    cVar2 = FUN_0042c710(uVar12);
    while (cVar2 != '\0') {
      iVar14 = FUN_0040c3a0();
      if (*(char *)(iVar14 + 4) == '\0') {
        iVar14 = FUN_0040c3a0();
        piVar5 = (int *)FUN_0042c810(*(undefined4 *)(iVar14 + 8));
        if (0 < *piVar5) {
          FUN_0042ca00();
          iVar14 = FUN_0040c3a0();
          piVar5 = (int *)FUN_0072fd10(*(undefined4 *)(iVar14 + 8));
          if (*piVar5 != 3) {
            uVar12 = 0;
            iVar14 = FUN_0040c3a0(0);
            cVar2 = FUN_007ce2a0(*(undefined4 *)(iVar14 + 8),uVar12);
            if (cVar2 != '\0') {
              puVar13 = (undefined4 *)FUN_0040c3a0();
              local_248 = *puVar13;
              uStack_244 = puVar13[1];
              uStack_23c = puVar13[3];
              local_238 = puVar13[4];
              uStack_234 = puVar13[5];
              local_230 = puVar13[6];
              local_8 = 0x12;
              iStack_240 = 0;
              local_2bc[1] = (int *)0x0;
              do {
                if (iStack_240 != 0) goto LAB_007b8881;
                FUN_0042a330();
                uVar12 = RNG__Next();
                iVar14 = FUN_0040c3a0();
                iStack_240 = FUN_00733610(*(undefined4 *)(iVar14 + 0x18),uVar12,7,0,0);
                if (iStack_240 == 0x26b) {
                  iStack_240 = 0;
                }
                local_2bc[1] = (int *)((int)local_2bc[1] + 1);
              } while ((int)local_2bc[1] < 10);
              if (iStack_240 != 0) {
LAB_007b8881:
                FUN_0075f0e0(iStack_240,0,1,0,0,0);
                FUN_0042ca00();
                iVar14 = FUN_0040c3a0();
                FUN_0072fd10(*(undefined4 *)(iVar14 + 8));
                FUN_00424530();
                FUN_007221a0(&local_248);
              }
              local_8 = 0xffffffff;
              guard_check_icall();
              param_1 = local_2d0;
            }
          }
        }
      }
      FUN_005cba20();
      uVar12 = FUN_00456190(&local_2ec);
      cVar2 = FUN_0042c710(uVar12);
    }
    FUN_005b16f0(0);
    uVar12 = FUN_006eef60();
    puVar16 = local_488;
LAB_007b850e:
    iVar14 = param_1[0x767];
    uVar11 = FUN_00417290(puVar16);
    piVar5 = (int *)FUN_00428b20(1000,0xf,uVar11,&DAT_00c7b640,iVar14,0,uVar12);
    (**(code **)(*piVar5 + 0xc))();
    param_1 = local_2d0;
    break;
  default:
    FUN_0042ca00();
    FUN_00685d40();
    iVar14 = FUN_00417840();
    if (iVar14 <= local_294) {
      Isaac__log(1,"Warning: Card % don\'t exist\n",local_294);
    }
  }
  if (local_2de != 0) {
    FUN_007ab6b0(local_294,"UseItem");
  }
LAB_007b8998:
  if ((local_2dd != '\0') && (*(int *)(local_36c + 0x5c) != 0)) {
    FUN_007cb5d0(*(int *)(local_36c + 0x5c),*(undefined4 *)(local_36c + 0x60),local_378);
  }
  FUN_00863cc0(local_294,param_1,param_3);
  ExceptionList = local_10;
  return;
LAB_007b3bf0:
  piVar5 = piVar5 + 2;
  local_2b0 = (int *)((int)local_2b0 + 1);
  if ((int *)0x3 < local_2b0) goto LAB_007b3c4c;
  goto LAB_007b3be0;
}
