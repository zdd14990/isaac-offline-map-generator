/* Static decompilation only; PE entry point was not executed. */
/* Target: 00762675 */
/* Reference: 00762675 */
/* Caller: FUN_0075f0e0 @ 0075f0e0 */


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall
FUN_0075f0e0(uint *param_1,uint *param_2,uint *param_3,undefined4 param_4,uint *param_5,uint param_6
            ,uint *param_7)

{
  short *psVar1;
  code *pcVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  uint uVar7;
  undefined8 uVar8;
  char cVar9;
  char cVar10;
  uint uVar11;
  undefined4 *puVar12;
  undefined1 *puVar13;
  int iVar14;
  undefined4 *puVar15;
  uint *puVar16;
  int iVar17;
  short sVar18;
  uint *puVar19;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  uint uVar20;
  int *piVar21;
  uint uVar22;
  int iVar23;
  uint *puVar24;
  bool bVar25;
  float in_XMM0_Da;
  float fVar26;
  uint *puVar27;
  undefined4 uVar28;
  undefined4 uVar29;
  undefined4 uVar30;
  undefined1 auStack_42c [40];
  undefined1 auStack_404 [40];
  undefined1 auStack_3dc [40];
  undefined1 auStack_3b4 [56];
  undefined4 uStack_37c;
  undefined4 uStack_378;
  undefined4 uStack_374;
  undefined4 uStack_370;
  undefined1 auStack_360 [8];
  undefined1 auStack_358 [8];
  undefined1 auStack_350 [8];
  undefined1 auStack_348 [8];
  undefined1 auStack_340 [8];
  undefined1 auStack_338 [8];
  undefined1 auStack_330 [8];
  undefined1 auStack_328 [8];
  undefined4 uStack_320;
  undefined1 uStack_31c;
  uint uStack_318;
  undefined4 uStack_314;
  undefined4 uStack_310;
  undefined4 uStack_30c;
  undefined4 uStack_308;
  undefined1 auStack_304 [8];
  undefined1 auStack_2fc [8];
  undefined1 auStack_2f4 [8];
  undefined1 auStack_2ec [8];
  undefined1 auStack_2e4 [8];
  undefined1 auStack_2dc [8];
  undefined1 auStack_2d4 [8];
  undefined1 auStack_2cc [8];
  undefined1 auStack_2c4 [8];
  undefined1 auStack_2bc [8];
  undefined1 auStack_2b4 [4];
  undefined4 uStack_2b0;
  undefined1 auStack_2ac [8];
  undefined1 auStack_2a4 [8];
  undefined1 auStack_29c [8];
  undefined1 auStack_294 [8];
  undefined1 auStack_28c [8];
  undefined1 auStack_284 [8];
  undefined1 auStack_27c [8];
  undefined1 auStack_274 [8];
  undefined1 auStack_26c [8];
  undefined1 auStack_264 [8];
  undefined1 auStack_25c [8];
  undefined1 auStack_254 [8];
  undefined1 auStack_24c [8];
  undefined1 auStack_244 [8];
  undefined1 auStack_23c [8];
  undefined4 uStack_234;
  undefined1 uStack_230;
  uint *puStack_22c;
  undefined4 uStack_228;
  undefined4 uStack_224;
  undefined4 uStack_220;
  uint *puStack_21c;
  undefined8 uStack_218;
  int iStack_20c;
  uint *puStack_204;
  undefined4 uStack_200;
  undefined4 uStack_1fc;
  int iStack_1f8;
  uint *puStack_1f4;
  uint *puStack_1f0;
  undefined1 auStack_1ec [4];
  uint *puStack_1e8;
  int *local_1e4;
  uint *local_1e0;
  uint *local_1dc;
  uint *puStack_1d8;
  uint *local_1d4;
  uint *local_1d0;
  undefined4 local_1cc;
  uint *local_1c8;
  undefined4 uStack_1c4;
  uint *local_1c0;
  int iStack_1bc;
  int iStack_1b8;
  int iStack_16c;
  int iStack_168;
  int iStack_164;
  int iStack_160;
  int iStack_15c;
  int iStack_158;
  int iStack_154;
  int iStack_150;
  int iStack_14c;
  int iStack_148;
  int iStack_144;
  undefined2 uStack_140;
  undefined2 uStack_13e;
  int iStack_13c;
  int iStack_120;
  undefined1 uStack_11c;
  undefined1 uStack_11b;
  undefined1 uStack_11a;
  int iStack_118;
  undefined1 uStack_114;
  undefined1 uStack_113;
  undefined1 uStack_112;
  int iStack_110;
  undefined1 uStack_10c;
  undefined1 uStack_10b;
  undefined1 uStack_10a;
  undefined1 uStack_109;
  undefined1 uStack_108;
  undefined1 uStack_107;
  int iStack_104;
  int iStack_100;
  int iStack_fc;
  int iStack_f8;
  int iStack_f4;
  int iStack_f0;
  int iStack_e0;
  int iStack_dc;
  uint local_d4 [4];
  undefined4 uStack_c4;
  uint uStack_c0;
  uint uStack_bc;
  undefined8 uStack_b8;
  uint uStack_b0;
  uint uStack_ac;
  uint uStack_a8;
  uint uStack_a4;
  uint uStack_a0;
  int iStack_9c;
  char acStack_98 [2];
  char cStack_96;
  undefined1 uStack_95;
  undefined4 uStack_8c;
  uint uStack_88;
  uint auStack_84 [4];
  undefined4 uStack_74;
  undefined4 uStack_70;
  undefined4 uStack_6c;
  undefined4 uStack_68;
  undefined4 uStack_64;
  float afStack_60 [8];
  uint uStack_40;
  float fStack_3c;
  float fStack_38;
  undefined8 uStack_34;
  undefined4 uStack_2c;
  float afStack_28 [4];
  uint *puStack_18;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;

  local_8 = 0xffffffff;
  puStack_c = &LAB_00aff018;
  local_10 = ExceptionList;
  uVar11 = DAT_00bf93b4 ^ (uint)&stack0xfffffffc;
  ExceptionList = &local_10;
  local_1e0 = param_2;
  local_1cc = param_7;
  local_1dc = param_1;
  local_14 = uVar11;
  local_1e4 = (int *)FUN_0072fd10(param_2);
  if (local_1e4 == (int *)0x0) {
    Isaac__log(1,"[warn] no config for collectible %d.\n",local_1e0);
    ExceptionList = local_10;
    return;
  }
  if ((int)param_5 < 1) {
    param_5 = (uint *)0x0;
  }
  iVar14 = DAT_00c71678[0x6e9e];
  local_1d0 = (uint *)0x3;
  if ((int)param_5 < 3) {
    local_1d0 = param_5;
  }
  if ((((iVar14 != 0) && (DAT_00c71678[0x6ea2] == 1)) && (iVar14 != 3)) && (iVar14 != 4)) {
    ExceptionList = local_10;
    return;
  }
  if (((param_1[0x4f0] == 0x28) && (param_1[0x79a] != 0)) && (*local_1e4 != 3)) {
    FUN_0075f0e0(local_1e0,param_3,param_4,local_1d0,param_6,0);
    ExceptionList = local_10;
    return;
  }
  local_1c8 = param_3;
  if (((int)param_3 < 0) && (local_1c8 = (uint *)local_1e4[0x32], (int)local_1c8 < 0)) {
    local_1c8 = (uint *)FUN_007911f0(local_1e0,param_6,local_1e4);
  }
  if (((int)local_1cc < 0) || ((uint *)0x1e < local_1cc)) {
    local_1d4 = (uint *)&DAT_00b1a4ec;
  }
  else {
    local_1d4 = (uint *)(&PTR_s_treasure_00b1f3d0)[(int)local_1cc];
  }
  puVar24 = param_1 + 0x4f1;
  if (0xf < param_1[0x4f6]) {
    puVar24 = (uint *)*puVar24;
  }
  local_1c0 = (uint *)param_1[0x587];
  puVar12 = (undefined4 *)FUN_0072ff10(local_d4,0);
  local_8 = 0;
  if (0xf < (uint)puVar12[5]) {
    puVar12 = (undefined4 *)*puVar12;
  }
  Isaac__log(1,"Adding collectible %d (%s) to player %d (%s) from pool %s\n",local_1e4[1],puVar12,
             local_1c0,puVar24,local_1d4,uVar11);
  local_8 = 0xffffffff;
  if (0xf < uStack_c0) {
    uVar22 = uStack_c0 + 1;
    uVar11 = local_d4[0];
    if (0xfff < uVar22) {
      uVar11 = *(uint *)(local_d4[0] - 4);
      uVar22 = uStack_c0 + 0x24;
      if (0x1f < (local_d4[0] - uVar11) - 4) {
                    /* WARNING: Subroutine does not return */
        _invalid_parameter_noinfo_noreturn();
      }
    }
    FUN_00aef15c(uVar11,uVar22);
  }
  uStack_c4 = 0;
  uStack_c0 = 0xf;
  local_d4[0] = local_d4[0] & 0xffffff00;
  puStack_1d8 = local_1e0;
  if ((((int)DAT_00c71678[0x9985] < 2) &&
      (*(int *)(DAT_00c7169c + 0x4b3d8) != *(int *)(DAT_00c7169c + 0x4b3dc))) &&
     (cVar9 = (**(code **)(*(int *)DAT_00c71678[0x9988] + 0x30))(local_1e0), cVar9 == '\0')) {
    puVar13 = (undefined1 *)FUN_00429f30(&puStack_1d8);
    *puVar13 = 1;
  }
  uStack_1c4 = param_4;
  if ((param_1[0xb] == 0) && (*(char *)((int)param_1 + 0x20a9) == '\0')) {
    FUN_007584b0();
    puVar12 = DAT_00c71678;
    if (((char)uStack_1c4 != '\0') && (iVar14 = FUN_0072fd10(local_1e0), iVar14 != 0)) {
      in_XMM0_Da = (float)puVar12[0x6b6d];
      puVar15 = puVar12 + 0x6b6d;
      if ((float)puVar12[0x6b6e] <= in_XMM0_Da && in_XMM0_Da != (float)puVar12[0x6b6e]) {
        puVar15 = puVar12 + 0x6b6e;
      }
      puVar12[0x6b6d] = *puVar15;
    }
  }
  puVar24 = local_1e0;
  FUN_0092a2d0(local_1e0);
  if ((int)puVar24 < 0) {
    FUN_009e03d0(puVar24);
    if ((puVar24 == (uint *)0xffffffff) &&
       (cVar9 = FUN_00456750(0x4f), iVar14 = DAT_00c7169c, cVar9 != '\0')) {
      FUN_007ea2d0();
      *(float *)(iVar14 + 0x2a2d4) = in_XMM0_Da;
      puVar24 = local_1e0;
    }
  }
  else {
    piVar21 = (int *)(param_1[0x5b2] + (int)puVar24 * 4);
    *piVar21 = *piVar21 + 1;
  }
  if (param_1[0xb] == 0) {
    if (*(char *)((int)param_1 + 0x20a9) == '\0') {
      uVar30 = 0;
      uVar28 = 1;
      cVar9 = FUN_0072fe80(1,0);
      if ((cVar9 != '\0') && (uVar11 = FUN_0075f020(1,0,uVar28,uVar30), 1 < uVar11)) {
        FUN_00929a20(0x1f);
      }
      uVar30 = 0;
      uVar28 = 2;
      cVar9 = FUN_0072fe80(2,0);
      if ((cVar9 != '\0') && (uVar11 = FUN_0075f020(2,0,uVar28,uVar30), 1 < uVar11)) {
        FUN_00929a20(0x92);
      }
      uVar30 = 0;
      uVar28 = 4;
      cVar9 = FUN_0072fe80(4,0);
      if ((cVar9 != '\0') && (uVar11 = FUN_0075f020(4,0,uVar28,uVar30), 2 < uVar11)) {
        FUN_00929a20(0x23);
      }
      uVar30 = 0;
      uVar28 = 8;
      cVar9 = FUN_0072fe80(8,0);
      if ((cVar9 != '\0') && (uVar11 = FUN_0075f020(8,0,uVar28,uVar30), 1 < uVar11)) {
        FUN_00929a20(0x171);
      }
      uVar30 = 0;
      uVar28 = 0x10;
      cVar9 = FUN_0072fe80(0x10,0);
      if ((cVar9 != '\0') && (uVar11 = FUN_0075f020(0x10,0,uVar28,uVar30), 1 < uVar11)) {
        FUN_00929a20(0x16f);
      }
      if (puVar24 == (uint *)0xfe) {
        uVar28 = 200;
code_r0x0075f57d:
        FUN_00929b40(uVar28,1);
      }
      else if (puVar24 == (uint *)0xdd) {
        uVar28 = 0xc9;
        goto code_r0x0075f57d;
      }
      FUN_00763290();
      uVar30 = 0;
      uVar28 = 0x800000;
      cVar9 = FUN_0072fe80(0x800000,0);
      if ((cVar9 != '\0') && (uVar11 = FUN_0075f020(0x800000,0,uVar28,uVar30), 2 < uVar11)) {
        FUN_00929a20(0x196);
      }
    }
    puVar24 = local_1dc;
    if ((param_1[0xb] == 0) && (*(char *)((int)param_1 + 0x20a9) == '\0')) {
      puStack_22c = local_1e0;
      uStack_224 = DAT_00c71678[1];
      uStack_220 = *(undefined4 *)(DAT_00c71678[0x60c0] + 8);
      uStack_228 = *DAT_00c71678;
      puStack_21c = local_1cc;
      uStack_234 = DAT_00c71678[0x993e];
      if ((char)local_1dc[0x609] == '\0') {
        uStack_234 = 0;
      }
      uStack_230 = 0;
      FUN_00721a70(&uStack_234);
      FUN_007ad4e0();
      param_1 = puVar24;
    }
  }
  piVar21 = local_1e4;
  if ((((char)uStack_1c4 != '\0') && (param_1[0xb] == 0)) &&
     (*(char *)((int)param_1 + 0x20a9) == '\0')) {
    iStack_1bc = *local_1e4;
    iStack_1b8 = local_1e4[1];
    FUN_0040cf50(local_1e4 + 2);
    local_8 = 1;
    FUN_0040cf50(piVar21 + 8);
    local_8._0_1_ = 2;
    FUN_0040cf50(piVar21 + 0xe);
    local_8._0_1_ = 3;
    iStack_16c = piVar21[0x14];
    iStack_168 = piVar21[0x15];
    iStack_164 = piVar21[0x16];
    iStack_160 = piVar21[0x17];
    iStack_15c = piVar21[0x18];
    iStack_158 = piVar21[0x19];
    iStack_154 = piVar21[0x1a];
    iStack_150 = piVar21[0x1b];
    iStack_14c = piVar21[0x1c];
    iStack_148 = piVar21[0x1d];
    iStack_144 = piVar21[0x1e];
    uStack_140 = (undefined2)piVar21[0x1f];
    uStack_13e = *(undefined2 *)((int)piVar21 + 0x7e);
    iStack_13c = piVar21[0x20];
    FUN_0040cf50(piVar21 + 0x21);
    iStack_120 = piVar21[0x27];
    uStack_11c = (undefined1)piVar21[0x28];
    uStack_11b = *(undefined1 *)((int)piVar21 + 0xa1);
    uStack_11a = *(undefined1 *)((int)piVar21 + 0xa2);
    iStack_118 = piVar21[0x29];
    uStack_114 = (undefined1)piVar21[0x2a];
    uStack_113 = *(undefined1 *)((int)piVar21 + 0xa9);
    uStack_112 = *(undefined1 *)((int)piVar21 + 0xaa);
    local_8 = CONCAT31(local_8._1_3_,4);
    iStack_110 = piVar21[0x2b];
    uStack_10c = (undefined1)piVar21[0x2c];
    uStack_10b = *(undefined1 *)((int)piVar21 + 0xb1);
    uStack_10a = *(undefined1 *)((int)piVar21 + 0xb2);
    uStack_109 = *(undefined1 *)((int)piVar21 + 0xb3);
    iStack_100 = piVar21[0x2f];
    uStack_108 = (undefined1)piVar21[0x2d];
    uStack_107 = *(undefined1 *)((int)piVar21 + 0xb5);
    iStack_104 = piVar21[0x2e];
    iStack_fc = piVar21[0x30];
    iStack_f8 = piVar21[0x31];
    iStack_f4 = piVar21[0x32];
    iStack_f0 = piVar21[0x33];
    FUN_007dcad0(piVar21 + 0x34);
    iStack_e0 = piVar21[0x37];
    iStack_dc = piVar21[0x38];
    local_8 = 5;
    if (1 < (int)DAT_00c71678[0x9985]) {
      (**(code **)(*(int *)DAT_00c71678[0x9988] + 0x40))(&iStack_1bc);
    }
    iVar14 = iStack_160;
    if ((param_1[0x4f0] == 0x24) && (iVar14 = 0xc, iStack_160 < 0xc)) {
      iVar14 = iStack_160;
    }
    puStack_1d8 = (uint *)param_1[0x4d0];
    FUN_00759500(iStack_154);
    FUN_007595b0(iStack_150);
    FUN_00759400(iStack_14c);
    FUN_007588a0(iStack_164,0);
    FUN_00758a70(iVar14,0,0);
    FUN_00758d00(iStack_15c,0);
    FUN_00758f90(iStack_158);
    iVar14 = FUN_007cafe0();
    if (((iVar14 == 3) || (iVar14 = FUN_007cafe0(), iVar14 == 0)) &&
       (puVar13 = (undefined1 *)((iStack_164 - param_1[0x4d0]) + (int)puStack_1d8), 0 < (int)puVar13
       )) {
      param_1[0x654] = (uint)(puVar13 + param_1[0x654]);
    }
    iStack_f0 = 0;
    local_8 = 0xffffffff;
    FUN_00722c10();
  }
  puVar24 = local_1d0;
  if (*local_1e4 == 3) {
    local_1d4 = (uint *)((int)(local_1d0 + 0x2b) * 0x20);
    if ((*(uint *)((int)local_1d4 + (int)param_1) == 0x248) ||
       (*(uint *)((int)local_1d4 + (int)param_1) == 0x3b)) {
      *(uint *)((int)local_1d4 + (int)param_1) = 0;
    }
    if (((local_1d0 == (uint *)0x0) && (cVar9 = FUN_007706e0(0x216,0), cVar9 != '\0')) &&
       (param_1[0x568] == 0)) {
      uVar11 = param_1[0x560];
      uVar22 = param_1[0x561];
      uVar20 = param_1[0x562];
      uVar3 = param_1[0x563];
      uVar4 = param_1[0x564];
      uVar5 = param_1[0x565];
      uVar6 = param_1[0x566];
      uVar7 = param_1[0x567];
      param_1[0x560] = param_1[0x568];
      param_1[0x561] = param_1[0x569];
      param_1[0x562] = param_1[0x56a];
      param_1[0x563] = param_1[0x56b];
      in_XMM0_Da = (float)param_1[0x56c];
      param_1[0x564] = (uint)in_XMM0_Da;
      param_1[0x565] = param_1[0x56d];
      param_1[0x566] = param_1[0x56e];
      param_1[0x567] = param_1[0x56f];
      param_1[0x568] = uVar11;
      param_1[0x569] = uVar22;
      param_1[0x56a] = uVar20;
      param_1[0x56b] = uVar3;
      param_1[0x56c] = uVar4;
      param_1[0x56d] = uVar5;
      param_1[0x56e] = uVar6;
      param_1[0x56f] = uVar7;
    }
    local_1c0 = *(uint **)((int)local_1d4 + (int)param_1);
    if ((int)local_1c0 < 0) {
      FUN_009e0450(local_1c0);
    }
    else if (0 < (int)local_1c0) {
      iVar23 = *(int *)(param_1[0x5b2] + (int)local_1c0 * 4) + -1;
      iVar14 = 0;
      if (0 < iVar23) {
        iVar14 = iVar23;
      }
      *(int *)(param_1[0x5b2] + (int)local_1c0 * 4) = iVar14;
    }
    *(uint **)((int)local_1d4 + (int)param_1) = local_1e0;
    param_1[(int)puVar24 * 8 + 0x561] = (uint)local_1cc;
    param_1[(int)puVar24 * 8 + 0x563] = 0;
    param_1[(int)puVar24 * 8 + 0x567] = param_6;
    FUN_00791420(local_1c8,local_1d0);
    param_1[(int)puVar24 * 8 + 0x564] = 0;
    param_1[(int)puVar24 * 8 + 0x566] = 0;
    if (param_1[0x580] == 0) {
      FUN_007c36b0();
      *(undefined1 *)((int)param_1 + 0x1826) = 0;
      param_1[0x621] = 0x1e;
    }
    piVar21 = local_1e4;
    if (*(char *)((int)local_1e4 + 0xb1) != '\0') {
      param_1[0x55d] = param_1[0x55d] | local_1e4[0x15];
    }
    cVar9 = FUN_00771550(0x65,0);
    if ((cVar9 != '\0') || (cVar9 = FUN_00771550(100,0), cVar9 != '\0')) {
      param_1[0x55d] = param_1[0x55d] | 0x41f;
      FUN_00763570();
    }
  }
  else {
    param_1[0x55d] = param_1[0x55d] | local_1e4[0x15];
    piVar21 = local_1e4;
  }
  cVar9 = FUN_007706e0(0x298,0);
  if ((cVar9 != '\0') && ((piVar21[0x2e] & 0x40000U) != 0)) {
    if (*(int *)(DAT_00c7169c + 0x2a408) - *(int *)(DAT_00c7169c + 0x2a404) >> 2 < 0x299) {
      iVar14 = 0;
    }
    else {
      iVar14 = *(int *)(*(int *)(DAT_00c7169c + 0x2a404) + 0xa60);
    }
    param_1[0x55d] = param_1[0x55d] | *(uint *)(iVar14 + 0x54);
  }
  iVar14 = DAT_00c7169c;
  if ((int)local_1e0 < 0) goto switchD_00762884_caseD_f1;
  puVar24 = (uint *)((int)local_1e0 * 0x10 + param_1[0x5dc]);
  local_1d4 = puVar24;
  if (param_1[0xb] != 0) goto code_r0x00762861;
  puVar19 = param_1;
  if ((int)local_1e0 < 0x12f) {
    if (local_1e0 == (uint *)0x12e) {
LAB_007608d5:
      FUN_0075e320(0xd,1);
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    }
    else {
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      switch(local_1e0) {
      case (uint *)0xc:
        goto LAB_007608d5;
      case (uint *)0x15:
        FUN_00748940(1);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        break;
      case (uint *)0x1d:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          uVar28 = 0;
          puVar24 = param_1 + 0xcf;
          iVar14 = RNG__RandomInt(4);
          FUN_007599d0(iVar14 + 3,puVar24,uVar28);
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        }
        break;
      case (uint *)0x1f:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          FUN_00813520(auStack_2f4,param_1 + 0xcf,0x42200000,0,0,0);
          uVar28 = RNG__Next();
          FUN_00428b20(5,10,auStack_2f4,&DAT_00c7b640,param_1,0,uVar28);
          local_1d0 = (uint *)0xdb;
          FUN_00956780();
          FUN_0092dc30(local_1d0,0x3f800000,2,0,0x3f800000,0);
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        }
        break;
      case (uint *)0x23:
      case (uint *)0x106:
        FUN_0075e320(0xf,1);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        break;
      case (uint *)0x36:
        FUN_00748860();
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        break;
      case (uint *)0x48:
        iVar14 = 0x1f;
        piVar21 = DAT_00c71678 + 0x69dd;
        do {
          *piVar21 = *piVar21 + 5;
          piVar21 = piVar21 + 0xd;
          iVar14 = iVar14 + -1;
          uVar8 = uStack_218;
        } while (iVar14 != 0);
        break;
      case (uint *)0x4b:
        goto LAB_00761720;
      case (uint *)0x4c:
      case (uint *)0x5b:
        FUN_0073f940();
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        break;
      case (uint *)0x51:
        sVar18 = 9;
        if (0 < (int)local_1c8) {
          sVar18 = (short)local_1c8;
        }
        *(short *)((int)param_1 + 0x137e) = *(short *)((int)param_1 + 0x137e) + sVar18;
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          iVar14 = FUN_007cafe0();
          if (iVar14 == 2) {
LAB_007603ee:
            FUN_00758a70(2,1,0);
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          }
          else {
            iVar14 = FUN_007cafe0();
            if (iVar14 == 1) {
              param_1[0x4d3] = 2;
              FUN_007592a0();
              FUN_00758a70(2,1,0);
              uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
            }
            else {
              iVar14 = FUN_007cafe0();
              if (iVar14 != 4) {
                param_1[0x4d0] = 0;
                FUN_007588a0(2,0);
                goto LAB_007603ee;
              }
              param_1[0x762] = 0;
              FUN_007ca840(1);
              FUN_00758a70(2,1,0);
              uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
            }
          }
        }
        break;
      case (uint *)0x74:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          uVar11 = 0;
          do {
            iVar14 = FUN_007c38c0(uVar11,0,0);
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
            if (iVar14 != 0) break;
            uVar11 = uVar11 + 1;
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          } while (uVar11 < 4);
        }
        break;
      case (uint *)0x7a:
switchD_00761f55_caseD_5:
        FUN_007c9ea0();
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        break;
      case (uint *)0x8b:
LAB_00761020:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          FUN_00813520(auStack_2ec,param_1 + 0xcf,0x42200000,0,0,0);
          uVar30 = RNG__Next();
          uVar28 = 0;
          puVar13 = auStack_2ec;
          iVar14 = 0x15e;
          goto LAB_007627f9;
        }
        break;
      case (uint *)0x8d:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          puVar19 = (uint *)0x0;
          auStack_84[1] = _DAT_00bab6c0;
          auStack_84[2] = _UNK_00bab6c4;
          auStack_84[3] = _UNK_00bab6c8;
          uStack_74 = _UNK_00bab6cc;
          auStack_84[0] = 0x18;
          uStack_70 = _DAT_00bab800;
          uStack_6c = _UNK_00bab804;
          uStack_68 = _UNK_00bab808;
          uStack_64 = _UNK_00bab80c;
          iStack_1f8 = 0;
          local_1c8 = (uint *)0x0;
          puStack_1f4 = (uint *)0x0;
          local_1cc = (uint *)0x0;
          puStack_1f0 = (uint *)0x0;
          local_8 = 7;
          puVar24 = auStack_84;
          local_1c0 = (uint *)0x9;
          do {
            puVar27 = local_1cc;
            puStack_1d8 = *(uint **)(DAT_00c7169c + 0x2a410);
            if ((((int)(*puVar24 & 0x7fff) <
                  *(int *)(DAT_00c7169c + 0x2a414) - (int)puStack_1d8 >> 2) &&
                (puStack_1d8[*puVar24 & 0x7fff] != 0)) &&
               (cVar9 = FUN_007300d0(0xffffffff), puVar19 = local_1c8, cVar9 != '\0')) {
              if (local_1c8 == puVar27) {
                FUN_0042c920(local_1c8,puVar24);
                local_1cc = puStack_1f0;
                puVar19 = puStack_1f4;
                local_1c8 = puStack_1f4;
              }
              else {
                *local_1c8 = *puVar24;
                puVar19 = local_1c8 + 1;
                puStack_1f4 = puVar19;
                local_1c8 = puVar19;
              }
            }
            puVar27 = local_1d4;
            param_1 = local_1dc;
            puVar24 = puVar24 + 1;
            local_1c0 = (uint *)((int)local_1c0 + -1);
          } while (local_1c0 != (uint *)0x0);
          local_1d0 = (uint *)0x0;
          if (3 < (uint)((int)puVar19 - iStack_1f8)) {
            iVar14 = RNG__RandomInt((int)puVar19 - iStack_1f8 >> 2);
            local_1d0 = *(uint **)(iStack_1f8 + iVar14 * 4);
          }
          puStack_1d8 = (uint *)((local_1d0 != (uint *)0x0) + 7);
          if (local_1d0 == (uint *)0x0) {
            local_1c0 = (uint *)0xffffffff;
          }
          else {
            local_1c0 = (uint *)RNG__RandomInt(puStack_1d8);
          }
          local_1c8 = (uint *)0x0;
          do {
            FUN_00813520(auStack_1ec,param_1 + 0xcf,0x42200000,0,0,0);
            uVar11 = *puVar27;
            if (local_1c8 == local_1c0) {
              if (uVar11 == 0) {
                Isaac__log(0x10,"RNG Seed is zero!\n");
                uVar11 = *puVar27;
                if (uVar11 == 0) {
                  pcVar2 = (code *)swi(3);
                  (*pcVar2)();
                  return;
                }
              }
              uVar11 = uVar11 >> ((byte)puVar27[1] & 0x1f) ^ uVar11;
              uVar11 = uVar11 << ((byte)puVar27[2] & 0x1f) ^ uVar11;
              uVar11 = uVar11 >> ((byte)puVar27[3] & 0x1f) ^ uVar11;
              *puVar27 = uVar11;
              uVar28 = 0x15e;
              puVar24 = local_1d0;
            }
            else {
              if (uVar11 == 0) {
                Isaac__log(0x10,"RNG Seed is zero!\n");
                uVar11 = *puVar27;
                if (uVar11 == 0) {
                  pcVar2 = (code *)swi(3);
                  (*pcVar2)();
                  return;
                }
              }
              uVar11 = uVar11 >> ((byte)puVar27[1] & 0x1f) ^ uVar11;
              uVar11 = uVar11 << ((byte)puVar27[2] & 0x1f) ^ uVar11;
              uVar11 = uVar11 >> ((byte)puVar27[3] & 0x1f) ^ uVar11;
              puVar24 = (uint *)0x0;
              *puVar27 = uVar11;
              uVar28 = 0x14;
            }
            iVar14 = FUN_00428b20(5,uVar28,auStack_1ec,&DAT_00c7b640,param_1,puVar24,uVar11);
            *(uint **)(iVar14 + 0x554) = local_1c8;
            local_1c8 = (uint *)((int)local_1c8 + 1);
          } while ((int)local_1c8 < (int)puStack_1d8);
          local_8 = 0xffffffff;
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          if (iStack_1f8 != 0) {
            uVar11 = (int)local_1cc - iStack_1f8 & 0xfffffffc;
            iVar14 = iStack_1f8;
            if (0xfff < uVar11) {
              iVar14 = *(int *)(iStack_1f8 + -4);
              uVar11 = uVar11 + 0x23;
              if (0x1f < (iStack_1f8 - iVar14) - 4U) {
                    /* WARNING: Subroutine does not return */
                _invalid_parameter_noinfo_noreturn();
              }
            }
            FUN_00aef15c(iVar14,uVar11);
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          }
        }
        break;
      case (uint *)0x8e:
        FUN_009302e0(0x8e,1,1);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        break;
      case (uint *)0x9b:
        local_1c0 = (uint *)0xed;
        FUN_00956780();
        FUN_0092dc30(local_1c0,0x3f800000,2,0,0x3f800000,0);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        break;
      case (uint *)0xb3:
        goto LAB_00760333;
      case (uint *)0xc2:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          FUN_00813520(auStack_23c,param_1 + 0xcf,0x42200000,0,0,0);
          uVar30 = RNG__Next();
          uVar11 = RNG__Next();
          uVar28 = FUN_00734180(uVar11,0x19,0,10,1);
          uStack_b8 = CONCAT44(DAT_00b1f66c._4_4_,(uint)DAT_00b1f66c);
          uStack_b0 = DAT_00b1f674;
          uStack_bc = uVar11;
          uVar28 = FUN_00865340(&uStack_bc,uVar28,1,0,0);
          puVar13 = auStack_23c;
          param_1 = local_1dc;
          puVar19 = local_1dc;
LAB_007627ee:
          iVar14 = 300;
          goto LAB_007627f9;
        }
        break;
      case (uint *)0xc3:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          local_1c0 = (uint *)0x0;
          do {
            FUN_00813520(auStack_244,param_1 + 0xcf,0x42200000,0,0,0);
            uVar11 = *puVar24;
            if (uVar11 == 0) {
              Isaac__log(0x10,"RNG Seed is zero!\n");
              uVar11 = *puVar24;
              if (uVar11 == 0) {
                pcVar2 = (code *)swi(3);
                (*pcVar2)();
                return;
              }
            }
            uVar11 = uVar11 >> ((byte)puVar24[1] & 0x1f) ^ uVar11;
            uVar11 = uVar11 << ((byte)puVar24[2] & 0x1f) ^ uVar11;
            uVar11 = uVar11 >> ((byte)puVar24[3] & 0x1f) ^ uVar11;
            *puVar24 = uVar11;
            iVar14 = FUN_00428b20(5,0x46,auStack_244,&DAT_00c7b640,param_1,0,uVar11);
            *(uint **)(iVar14 + 0x554) = local_1c0;
            local_1c0 = (uint *)((int)local_1c0 + 1);
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          } while ((int)local_1c0 < 4);
        }
        break;
      case (uint *)0xc4:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          local_1c0 = (uint *)0x0;
          do {
            FUN_00813520(auStack_24c,param_1 + 0xcf,0x42200000,0,0,0);
            uVar11 = *puVar24;
            if (uVar11 == 0) {
              Isaac__log(0x10,"RNG Seed is zero!\n");
              uVar11 = *puVar24;
              if (uVar11 == 0) {
                pcVar2 = (code *)swi(3);
                (*pcVar2)();
                return;
              }
            }
            uVar11 = uVar11 >> ((byte)puVar24[1] & 0x1f) ^ uVar11;
            uVar11 = uVar11 << ((byte)puVar24[2] & 0x1f) ^ uVar11;
            uVar11 = uVar11 >> ((byte)puVar24[3] & 0x1f) ^ uVar11;
            *puVar24 = uVar11;
            iVar14 = FUN_00428b20(5,10,auStack_24c,&DAT_00c7b640,param_1,3,uVar11);
            *(uint **)(iVar14 + 0x554) = local_1c0;
            local_1c0 = (uint *)((int)local_1c0 + 1);
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          } while ((int)local_1c0 < 2);
        }
        break;
      case (uint *)0xc6:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          local_1c8 = (uint *)0x0;
          do {
            FUN_00813520(auStack_254,param_1 + 0xcf,0x42200000,0,0,0);
            uVar11 = *puVar24;
            if (uVar11 == 0) {
              Isaac__log(0x10,"RNG Seed is zero!\n");
              uVar11 = *puVar24;
              if (uVar11 == 0) {
                pcVar2 = (code *)swi(3);
                (*pcVar2)();
                return;
              }
            }
            uVar11 = uVar11 >> ((byte)puVar24[1] & 0x1f) ^ uVar11;
            uVar11 = uVar11 << ((byte)puVar24[2] & 0x1f) ^ uVar11;
            uVar11 = uVar11 >> ((byte)puVar24[3] & 0x1f) ^ uVar11;
            *puVar24 = uVar11;
            iVar14 = FUN_00428b20(5,*(undefined4 *)(&DAT_00b67400 + (int)local_1c8 * 4),auStack_254,
                                  &DAT_00c7b640,param_1,0,uVar11);
            *(uint **)(iVar14 + 0x554) = local_1c8;
            local_1c8 = (uint *)((int)local_1c8 + 1);
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          } while ((int)local_1c8 < 7);
        }
        break;
      case (uint *)0xc9:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          iVar14 = FUN_007911c0(0x93);
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          if (-1 < iVar14) {
            FUN_007c38c0(iVar14,1,0);
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          }
        }
        break;
      case (uint *)0xe6:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          uVar11 = param_1[0x766];
          if (uVar11 == 0) {
            iVar14 = 0;
          }
          else {
            iVar14 = *(int *)(uVar11 + 0x1340);
          }
          local_1c8 = (uint *)(iVar14 + 4 + param_1[0x4d0]);
          if ((int)DAT_00c71678[0x9985] < 2) {
            param_1[0x4d1] = 0;
            uVar22 = 0;
          }
          else {
            local_1c8 = (uint *)((uint)local_1c8 >> 4);
            uVar22 = (int)param_1[0x4d0] / 2;
          }
          param_1[0x4d0] = uVar22;
          if (uVar11 != 0) {
            *(undefined4 *)(uVar11 + 0x1344) = 0;
            *(undefined4 *)(param_1[0x766] + 0x1340) = 0;
          }
          FUN_007c9ea0();
          FUN_00758f90(local_1c8);
          FUN_007caad0();
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        }
        break;
      case (uint *)0xe8:
        FUN_007ea2d0();
        *(float *)(iVar14 + 0x2a2d4) = in_XMM0_Da;
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        break;
      case (uint *)0xf6:
LAB_007609eb:
        FUN_007488d0();
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        break;
      case (uint *)0xfb:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          if (DAT_00c71678[0x9961] == 0x2b) {
            local_1c0 = (uint *)0x3;
            do {
              puVar24 = local_1d4;
              uVar11 = *local_1d4;
              if (uVar11 == 0) {
                Isaac__log(0x10,"RNG Seed is zero!\n");
                uVar11 = *puVar24;
                if (uVar11 == 0) {
                  pcVar2 = (code *)swi(3);
                  (*pcVar2)();
                  return;
                }
              }
              uVar11 = uVar11 >> ((byte)puVar24[1] & 0x1f) ^ uVar11;
              uVar11 = uVar11 << ((byte)puVar24[2] & 0x1f) ^ uVar11;
              uVar11 = uVar11 >> ((byte)local_1d4[3] & 0x1f) ^ uVar11;
              *local_1d4 = uVar11;
              uVar28 = FUN_00813520(auStack_330,param_1 + 0xcf,0x42200000,0,0,0);
              FUN_00428b20(5,300,uVar28,&DAT_00c7b640,param_1,1,uVar11);
              local_1c0 = (uint *)((int)local_1c0 + -1);
            } while (local_1c0 != (uint *)0x0);
            local_1c0 = (uint *)0x0;
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          }
          else {
            uVar28 = RNG__Next();
            uVar30 = FUN_00813520(auStack_338,param_1 + 0xcf,0x42200000,0,0,0);
            FUN_00428b20(5,300,uVar30,&DAT_00c7b640,param_1,0,uVar28);
            puVar24 = local_1d4;
            local_1c8 = param_1 + 0x5e8;
            local_1c0 = (uint *)0x4;
            do {
              if ((*local_1c8 != 0) && (local_1c8[1] == 0)) {
                local_1c8[1] = 1;
                uVar11 = *puVar24;
                if (uVar11 == 0) {
                  Isaac__log(0x10,"RNG Seed is zero!\n");
                  uVar11 = *puVar24;
                  if (uVar11 == 0) {
                    pcVar2 = (code *)swi(3);
                    (*pcVar2)();
                    return;
                  }
                }
                uVar11 = uVar11 >> ((byte)puVar24[1] & 0x1f) ^ uVar11;
                uVar11 = uVar11 << ((byte)puVar24[2] & 0x1f) ^ uVar11;
                uVar11 = uVar11 >> ((byte)puVar24[3] & 0x1f) ^ uVar11;
                *puVar24 = uVar11;
                uVar28 = FUN_00734180(uVar11,0x19,0,10,1);
                uStack_a8 = (uint)DAT_00b1f66c;
                uStack_a4 = DAT_00b1f66c._4_4_;
                uStack_a0 = DAT_00b1f674;
                uStack_ac = uVar11;
                uVar11 = FUN_00865340(&uStack_ac,uVar28,1,0,0);
                *local_1c8 = uVar11;
              }
              local_1c8 = local_1c8 + 2;
              local_1c0 = (uint *)((int)local_1c0 + -1);
            } while (local_1c0 != (uint *)0x0);
            local_1c0 = (uint *)0x0;
            param_1 = local_1dc;
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          }
        }
        break;
      case (uint *)0xfc:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          uVar28 = RNG__Next();
          uVar30 = FUN_00813520(auStack_358,param_1 + 0xcf,0x42200000,0,0,0);
          FUN_00428b20(5,0x46,uVar30,&DAT_00c7b640,param_1,0,uVar28);
          puVar24 = local_1d4;
          param_1 = param_1 + 0x5e8;
          local_1c0 = (uint *)0x4;
          do {
            puVar12 = DAT_00c71678;
            if ((*param_1 != 0) && (param_1[1] == 1)) {
              param_1[1] = 0;
              puStack_1d8 = puVar12 + 0x69d0;
              uVar11 = *puVar24;
              if (uVar11 == 0) {
                Isaac__log(0x10,"RNG Seed is zero!\n");
                uVar11 = *puVar24;
                if (uVar11 == 0) {
                  pcVar2 = (code *)swi(3);
                  (*pcVar2)();
                  return;
                }
              }
              uVar11 = uVar11 >> ((byte)puVar24[1] & 0x1f) ^ uVar11;
              uVar11 = uVar11 << ((byte)puVar24[2] & 0x1f) ^ uVar11;
              uVar11 = uVar11 >> ((byte)puVar24[3] & 0x1f) ^ uVar11;
              *puVar24 = uVar11;
              uVar11 = FUN_00734900(uVar11);
              *param_1 = uVar11;
            }
            param_1 = param_1 + 2;
            local_1c0 = (uint *)((int)local_1c0 + -1);
          } while (local_1c0 != (uint *)0x0);
          local_1c0 = (uint *)0x0;
          param_1 = local_1dc;
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        }
        break;
      case (uint *)0x104:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          FUN_00748bc0(0xffffffff);
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        }
        break;
      case (uint *)0x107:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          uVar28 = RNG__Next();
          uVar28 = FUN_00734180(uVar28,0,0xffffffff,0,1);
          FUN_00813520(auStack_25c,param_1 + 0xcf,0x42200000,0,0,0);
          uVar30 = RNG__Next();
          puVar13 = auStack_25c;
          puVar19 = (uint *)0x0;
          goto LAB_007627ee;
        }
      }
    }
    goto switchD_00761f55_caseD_2;
  }
  if ((int)local_1e0 < 0x245) {
    if (local_1e0 == (uint *)0x244) {
      FUN_008271e0();
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    }
    else {
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      switch(local_1e0) {
      case (uint *)0x139:
        FUN_009302e0(0x139,1,1);
        iStack_9c._0_1_ = s_Shimmer_00b6ae3c[0];
        iStack_9c._1_1_ = s_Shimmer_00b6ae3c[1];
        iStack_9c._2_1_ = s_Shimmer_00b6ae3c[2];
        iStack_9c._3_1_ = s_Shimmer_00b6ae3c[3];
        acStack_98[0] = s_Shimmer_00b6ae3c[4];
        acStack_98[1] = s_Shimmer_00b6ae3c[5];
        uStack_88 = 0xf;
        uStack_8c = 7;
        cStack_96 = s_Shimmer_00b6ae3c[6];
        uStack_95 = 0;
        local_8 = 6;
        FUN_00759f50(0x139,1,&iStack_9c,0xffffffff,extraout_ECX);
        local_8 = 0xffffffff;
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if (0xf < uStack_88) {
          uVar11 = uStack_88 + 1;
          iVar14 = iStack_9c;
          if (0xfff < uVar11) {
            iVar14 = *(int *)(iStack_9c + -4);
            uVar11 = uStack_88 + 0x24;
            if (0x1f < (iStack_9c - iVar14) - 4U) {
                    /* WARNING: Subroutine does not return */
              _invalid_parameter_noinfo_noreturn();
            }
          }
          FUN_00aef15c(iVar14,uVar11);
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        }
        break;
      case (uint *)0x14d:
        FUN_00748860();
        FUN_00748940(1);
        goto LAB_007609eb;
      case (uint *)0x157:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          local_1c0 = (uint *)0x0;
          do {
            puVar24 = local_1d4;
            uVar11 = *local_1d4;
            if (uVar11 == 0) {
              Isaac__log(0x10,"RNG Seed is zero!\n");
              uVar11 = *puVar24;
              if (uVar11 == 0) {
                pcVar2 = (code *)swi(3);
                (*pcVar2)();
                return;
              }
            }
            uVar11 = uVar11 >> ((byte)puVar24[1] & 0x1f) ^ uVar11;
            uVar11 = uVar11 << ((byte)puVar24[2] & 0x1f) ^ uVar11;
            uVar11 = uVar11 >> ((byte)local_1d4[3] & 0x1f) ^ uVar11;
            *local_1d4 = uVar11;
            uVar28 = FUN_00813520(auStack_348,param_1 + 0xcf,0x42200000,0,0,0);
            iVar14 = FUN_00428b20(5,0x1e,uVar28,&DAT_00c7b640,param_1,0,uVar11);
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
            *(uint **)(iVar14 + 0x554) = local_1c0;
            local_1c0 = (uint *)((int)local_1c0 + 1);
          } while ((int)local_1c0 < 2);
        }
        break;
      case (uint *)0x158:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          local_1c0 = (uint *)0x0;
          do {
            puVar24 = local_1d4;
            uVar11 = *local_1d4;
            if (uVar11 == 0) {
              Isaac__log(0x10,"RNG Seed is zero!\n");
              uVar11 = *puVar24;
              if (uVar11 == 0) {
                pcVar2 = (code *)swi(3);
                (*pcVar2)();
                return;
              }
            }
            uVar11 = uVar11 >> ((byte)puVar24[1] & 0x1f) ^ uVar11;
            uVar11 = uVar11 << ((byte)puVar24[2] & 0x1f) ^ uVar11;
            uVar11 = uVar11 >> ((byte)local_1d4[3] & 0x1f) ^ uVar11;
            *local_1d4 = uVar11;
            uVar28 = FUN_00813520(auStack_340,param_1 + 0xcf,0x42200000,0,0,0);
            iVar14 = FUN_00428b20(5,0x28,uVar28,&DAT_00c7b640,param_1,0,uVar11);
            *(uint **)(iVar14 + 0x554) = local_1c0;
            local_1c0 = (uint *)((int)local_1c0 + 1);
          } while ((int)local_1c0 < 3);
          cVar9 = FUN_00734130(0x29);
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          if (cVar9 != '\0') {
            uVar28 = RNG__Next();
            uVar30 = FUN_00813520(auStack_2b4,param_1 + 0xcf,0x42200000,0,0,0);
            iVar14 = FUN_00428b20(5,0x15e,uVar30,&DAT_00c7b640,param_1,0x29,uVar28);
            *(undefined4 *)(iVar14 + 0x554) = 3;
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          }
        }
        break;
      case (uint *)0x15e:
        puVar24 = (uint *)DAT_00c71678[0x60c0];
        puStack_1d8 = puVar24;
        iVar14 = FUN_00456540();
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if (0 < iVar14) {
          cVar9 = '\0';
          local_1cc = (uint *)((uint)local_1cc & 0xffffff);
          local_1c0 = (uint *)0x0;
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          if (puVar24[0x499] != 0) {
            do {
              iVar14 = *(int *)(puVar24[0x497] + (int)local_1c0 * 4);
              if (((1 < (int)DAT_00c71678[0x9985]) && (*(int *)(iVar14 + 0x28) == 1)) ||
                 (*(int *)(iVar14 + 0x28) - 10U < 0x3de)) {
                uStack_2b0 = *(undefined4 *)(iVar14 + 0x16c);
                if (((*(uint *)(iVar14 + 0x168) & 0x11) == 0) &&
                   ((*(uint *)(iVar14 + 0x168) & 0x20000011) == 0)) {
                  FUN_00431310(param_1);
                  FUN_006ad500(auStack_3b4,0x5a,0,0);
                  local_1cc = (uint *)CONCAT13(1,(undefined3)local_1cc);
                  cVar9 = '\x01';
                }
                else {
                  cVar9 = local_1cc._3_1_;
                }
              }
              local_1c0 = (uint *)((int)local_1c0 + 1);
              puVar24 = puStack_1d8;
            } while (local_1c0 < (uint *)puStack_1d8[0x499]);
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
            if (cVar9 != '\0') {
              FUN_00407170();
              uStack_37c = _DAT_00bac030;
              uStack_378 = _UNK_00bac034;
              uStack_374 = _UNK_00bac038;
              uStack_370 = _UNK_00bac03c;
              FUN_009960b0(extraout_ECX_00);
              uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
            }
          }
        }
        break;
      case (uint *)0x162:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          FUN_00813520(auStack_264,param_1 + 0xcf,0x42200000,0,0,0);
          uVar30 = RNG__Next();
          uVar28 = 0;
          puVar13 = auStack_264;
          iVar14 = 0x15e;
          goto LAB_007627f9;
        }
        break;
      case (uint *)0x172:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          local_1c0 = (uint *)0x0;
          do {
            uVar11 = *puVar24;
            if (uVar11 == 0) {
              Isaac__log(0x10,"RNG Seed is zero!\n");
              uVar11 = *puVar24;
              if (uVar11 == 0) {
                pcVar2 = (code *)swi(3);
                (*pcVar2)();
                return;
              }
            }
            uVar11 = uVar11 >> ((byte)puVar24[1] & 0x1f) ^ uVar11;
            local_1c8 = (uint *)0x0;
            uVar11 = uVar11 << ((byte)puVar24[2] & 0x1f) ^ uVar11;
            uVar11 = uVar11 >> ((byte)puVar24[3] & 0x1f) ^ uVar11;
            *puVar24 = uVar11;
            uVar11 = uVar11 % 3;
            if (uVar11 == 0) {
              local_1c8 = (uint *)0x1;
            }
            else if (uVar11 == 1) {
              local_1c8 = (uint *)0x3;
            }
            else if (uVar11 == 2) {
              local_1c8 = (uint *)&DAT_00000006;
            }
            FUN_00813520(auStack_26c,param_1 + 0xcf,0x42200000,0,0,0);
            uVar28 = RNG__Next();
            iVar14 = FUN_00428b20(5,10,auStack_26c,&DAT_00c7b640,param_1,local_1c8,uVar28);
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
            *(uint **)(iVar14 + 0x554) = local_1c0;
            local_1c0 = (uint *)((int)local_1c0 + 1);
          } while ((int)local_1c0 < 3);
        }
        break;
      case (uint *)0x17d:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          cVar9 = FUN_006dae20();
          uVar8 = uStack_218;
          if (cVar9 == '\0') {
            iVar14 = DAT_00c7169c + 0x14;
            if (*(int *)(DAT_00c7169c + 0x4b3d8) != *(int *)(DAT_00c7169c + 0x4b3dc)) {
              uStack_218 = FUN_00a23920();
              iVar14 = FUN_0090c300(&uStack_218);
            }
            puStack_1d8 = (uint *)0x1;
            iVar23 = 0x10000;
            if (*(int *)(DAT_00c7169c + 0x4b3d8) == *(int *)(DAT_00c7169c + 0x4b3dc)) {
              iVar23 = 1;
            }
            *(int *)(iVar14 + 0x484) = *(int *)(iVar14 + 0x484) + iVar23;
            uVar8 = uStack_218;
          }
        }
        break;
      case (uint *)0x192:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          iVar14 = RNG__RandomInt(6);
          puStack_1d8 = (uint *)(iVar14 + 1);
          local_1c0 = (uint *)0x0;
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          if (0 < (int)puStack_1d8) {
            do {
              FUN_00813520(auStack_274,param_1 + 0xcf,0x42200000,0,0,0);
              RNG__Next();
              uVar28 = *(undefined4 *)(&DAT_00b6bd90 + (*puVar24 & 7) * 4);
              uVar30 = RNG__Next();
              iVar14 = FUN_00428b20(5,uVar28,auStack_274,&DAT_00c7b640,param_1,0,uVar30);
              uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
              *(uint **)(iVar14 + 0x554) = local_1c0;
              local_1c0 = (uint *)((int)local_1c0 + 1);
              puVar24 = local_1d4;
            } while ((int)local_1c0 < (int)puStack_1d8);
          }
        }
        break;
      case (uint *)0x19c:
        param_1[0x64d] = 0;
        FUN_007c7d70(1);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        break;
      case (uint *)0x19d:
        param_1[0x64c] = 0;
        FUN_007c7d70(0);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        break;
      case (uint *)0x1a8:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          FUN_00813520(auStack_27c,param_1 + 0xcf,0x42200000,0,0,0);
          uVar30 = RNG__Next();
          uVar28 = 0;
          puVar13 = auStack_27c;
          iVar14 = 0x45;
          goto LAB_007627f9;
        }
        break;
      case (uint *)0x1a9:
        FUN_00748bc0(1);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        break;
      case (uint *)0x1b7:
        cVar9 = FUN_00771550(0x79,0);
        if ((cVar9 != '\0') && (cVar9 = FUN_00771620(0x79), cVar9 == '\0')) {
          FUN_007db0a0();
        }
        iVar14 = PlayerManager__condition_7cb6e0(0x6d);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((1 < iVar14) &&
           (uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218), param_1[0x7bc] == 0)) {
          param_1[0x7bc] = 1;
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        }
        break;
      case (uint *)0x1c3:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          FUN_00813520(auStack_2e4,param_1 + 0xcf,0x42200000,0,0,0);
          uVar28 = RNG__Next();
          uVar28 = FUN_00734180(uVar28,0,0,0,0);
          uVar30 = RNG__Next();
          puVar13 = auStack_2e4;
          puVar19 = (uint *)0x0;
          goto LAB_007627ee;
        }
        break;
      case (uint *)0x1c6:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          FUN_00813520(auStack_304,param_1 + 0xcf,0x42200000,0,0,0);
          uVar30 = RNG__Next();
          iVar14 = RNG__RandomInt(2);
          puVar13 = auStack_304;
          uVar28 = 0;
          iVar14 = (-(uint)(iVar14 != 0) & 0xffffff1a) + 300;
          goto LAB_007627f9;
        }
        break;
      case (uint *)0x1c7:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          FUN_00813520(auStack_284,param_1 + 0xcf,0x42200000,0,0,0);
          uVar30 = RNG__Next();
          uVar28 = 5;
          puVar13 = auStack_284;
          iVar14 = 0x14;
          goto LAB_007627f9;
        }
        break;
      case (uint *)0x1ca:
        goto LAB_00761020;
      case (uint *)0x1f1:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if (1 < (int)DAT_00c71678[0x9985]) {
          FUN_009302e0(0x1f1,1,1);
          uVar11 = 0;
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          if ((int)(DAT_00c71678[0x6eab] - DAT_00c71678[0x6eaa]) >> 2 != 0) {
            do {
              puStack_1d8 = (uint *)FUN_009b92c0(uVar11);
              if ((puStack_1d8 != param_1) && (puStack_1d8 != (uint *)param_1[0x79a])) {
                FUN_00431310(param_1);
                FUN_006add70(auStack_3dc,0x5a,0);
              }
              uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
              uVar11 = uVar11 + 1;
            } while (uVar11 < (uint)((int)(DAT_00c71678[0x6eab] - DAT_00c71678[0x6eaa]) >> 2));
          }
        }
        break;
      case (uint *)0x1f5:
        FUN_007ce420();
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        break;
      case (uint *)0x219:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          FUN_00813520(auStack_2ac,param_1 + 0xcf,0x42200000,0,0,0);
          uVar30 = RNG__Next();
          uVar28 = 0;
          puVar13 = auStack_2ac;
          iVar14 = 0x46;
          goto LAB_007627f9;
        }
        break;
      case (uint *)0x21a:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          local_1c0 = (uint *)0x0;
          do {
            FUN_00813520(auStack_2dc,param_1 + 0xcf,0x42200000,0,0,0);
            uVar28 = RNG__Next();
            iVar14 = FUN_00428b20(5,0x15e,auStack_2dc,&DAT_00c7b640,param_1,0,uVar28);
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
            *(uint **)(iVar14 + 0x554) = local_1c0;
            local_1c0 = (uint *)((int)local_1c0 + 1);
          } while ((int)local_1c0 < 3);
        }
        break;
      case (uint *)0x21d:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          FUN_007ca840(1);
          local_1c0 = (uint *)0x0;
          do {
            FUN_00813520(auStack_2d4,param_1 + 0xcf,0x42200000,0,0,0);
            uVar28 = RNG__Next();
            iVar14 = FUN_00428b20(5,10,auStack_2d4,&DAT_00c7b640,param_1,1,uVar28);
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
            *(uint **)(iVar14 + 0x554) = local_1c0;
            local_1c0 = (uint *)((int)local_1c0 + 1);
          } while ((int)local_1c0 < 3);
        }
        break;
      case (uint *)0x223:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          FUN_007ca840(1);
          if ((*(char *)(DAT_00c7169c + 199) != '\0') ||
             (((uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218),
               *(int *)(DAT_00c7169c + 8) == 2 &&
               (uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218),
               DAT_00c71678 != (undefined4 *)0x0)) &&
              ((DAT_00c71678[0x998c] != 0 ||
               (uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218),
               *(char *)((int)DAT_00c71678 + 0x26589) != '\0')))))) {
            cVar9 = FUN_00734130(0x15);
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
            if (cVar9 != '\0') {
              FUN_00813520(auStack_2cc,param_1 + 0xcf,0x42200000,0,0,0);
              uVar30 = RNG__Next();
              uVar28 = 0x15;
              puVar13 = auStack_2cc;
              iVar14 = 0x15e;
              goto LAB_007627f9;
            }
          }
        }
        break;
      case (uint *)0x225:
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if ((char)uStack_1c4 != '\0') {
          iVar14 = FUN_007cafe0();
          if ((iVar14 == 3) || (iVar14 = FUN_007cafe0(), iVar14 == 2)) {
            *(short *)(param_1 + 0x624) = (short)param_1[0x624] + 1;
            param_1[0x55d] = param_1[0x55d] | 2;
          }
          else {
            param_1[0x4d1] = 0;
            param_1[0x4d0] = 0;
            if (param_1[0x766] != 0) {
              *(undefined4 *)(param_1[0x766] + 0x1344) = 0;
              *(undefined4 *)(param_1[0x766] + 0x1340) = 0;
              FUN_007ca840(6);
              uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
              break;
            }
          }
          FUN_007ca840(6);
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        }
        break;
      case (uint *)0x227:
        puVar24 = param_1 + 0x560;
        local_1cc = (uint *)0x0;
        if (param_1[0x560] == 0x226) {
          local_1cc = (uint *)(param_1[0x563] + param_1[0x562]);
        }
        if (param_1[0x568] == 0x226) {
          local_1cc = (uint *)(param_1[0x56b] + param_1[0x56a]);
        }
        if (param_1[0x570] == 0x226) {
          local_1cc = (uint *)(param_1[0x573] + param_1[0x572]);
        }
        if (param_1[0x578] == 0x226) {
          local_1cc = (uint *)(param_1[0x57b] + param_1[0x57a]);
        }
        cVar9 = FUN_007706e0(0x226,0);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if (cVar9 != '\0') {
          FUN_0078f840(0x226,0,0,1);
          FUN_0078f840(0x227,0,0,1);
          FUN_0075f0e0(0x228,0,0,0,0,0);
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          uVar11 = 0;
          do {
            if (*puVar24 == 0x228) {
              uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
              if (-1 < (int)uVar11) {
                FUN_00791420(local_1cc,uVar11);
                uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
              }
              break;
            }
            uVar11 = uVar11 + 1;
            puVar24 = puVar24 + 8;
          } while (uVar11 < 4);
        }
      }
    }
    goto switchD_00761f55_caseD_2;
  }
  uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
  switch(local_1e0) {
  case (uint *)0x24c:
    FUN_00748a30();
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    break;
  case (uint *)0x24d:
    FUN_00748a70();
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    break;
  case (uint *)0x251:
    *(undefined1 *)(param_1 + 0x7a6) = 1;
    param_1[0x7a4] = 0;
    param_1[0x7a5] = 0xffffffff;
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    break;
  case (uint *)0x252:
    param_1[0x7ba] = 0x3f800000;
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    break;
  case (uint *)0x253:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((char)uStack_1c4 != '\0') {
      FUN_007d3e40();
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    }
    break;
  case (uint *)0x259:
LAB_00760333:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((char)uStack_1c4 != '\0') {
      FUN_00758c20(1);
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    }
    break;
  case (uint *)0x25a:
    FUN_007f8190(0);
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    break;
  case (uint *)0x25b:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((char)uStack_1c4 != '\0') {
      uVar11 = 0;
      do {
        iVar14 = FUN_007c38c0(uVar11,0,0);
        if (iVar14 != 0) break;
        uVar11 = uVar11 + 1;
      } while (uVar11 < 4);
      puStack_1d8 = param_1 + 0xcf;
      uVar11 = 0;
      do {
        FUN_00813520(auStack_2fc,puStack_1d8,0x42200000,0,0,0);
        uVar28 = RNG__Next();
        iVar14 = FUN_00428b20(5,0x5a,auStack_2fc,&DAT_00c7b640,0,uVar11 == 0,uVar28);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        *(uint *)(iVar14 + 0x554) = uVar11;
        uVar11 = uVar11 + 1;
        param_1 = local_1dc;
      } while (uVar11 < 3);
    }
    break;
  case (uint *)0x26b:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    switch(param_1[0x4f0]) {
    case 1:
    case 0xe:
    case 0x16:
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      if ((char)uStack_1c4 != '\0') {
        FUN_007588a0(2,0);
        FUN_00758a70(2,0,0);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      }
      break;
    case 3:
    case 0xc:
      puVar24 = param_1 + 0x568;
      local_1d0 = (uint *)0x1;
      do {
        if (*puVar24 == 0x22) {
          uStack_ac = *puVar24;
          uStack_a8 = puVar24[1];
          uStack_a4 = puVar24[2];
          uStack_a0 = puVar24[3];
          uStack_bc = puVar24[4];
          uStack_b8 = *(undefined8 *)(puVar24 + 5);
          uStack_b0 = puVar24[7];
          FUN_0078f840(0x22,1,local_1d0,0);
          if (*puVar24 == 0x3b) {
            *puVar24 = uStack_ac;
            puVar24[1] = uStack_a8;
            puVar24[2] = uStack_a4;
            puVar24[3] = uStack_a0;
            puVar24[4] = uStack_bc;
            puVar24[5] = (uint)uStack_b8;
            puVar24[6] = uStack_b8._4_4_;
            puVar24[7] = uStack_b0;
            *puVar24 = 0x3b;
          }
        }
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        local_1d0 = (uint *)((int)local_1d0 + -1);
        puVar24 = puVar24 + -8;
      } while (-1 < (int)local_1d0);
      break;
    case 5:
      goto switchD_00761f55_caseD_5;
    case 9:
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      if ((char)uStack_1c4 != '\0') {
        puStack_1e8 = param_1 + 0xcf;
        local_1cc = (uint *)0x3;
        uVar11 = 0xffffffff;
        do {
          FUN_00813520(auStack_29c,puStack_1e8,0x42200000,0,0,0);
          local_1d0 = (uint *)0x0;
          do {
            iVar14 = RNG__RandomInt((*(int *)(DAT_00c7169c + 0x2a408) -
                                     *(int *)(DAT_00c7169c + 0x2a404) >> 2) + -1);
            local_1c8 = (uint *)(iVar14 + 1);
            local_1c0 = (uint *)FUN_0072fd10(local_1c8);
            cVar9 = FUN_0072fe30(local_1c8);
            if (((cVar9 != '\0') && ((local_1c0[0x2f] & 1) == 0)) &&
               ((cVar9 = FUN_007300d0(0xffffffff), cVar9 != '\0' && (*local_1c0 != 3)))) {
              if (local_1c8 != (uint *)0x0) goto LAB_007620a4;
              break;
            }
            local_1d0 = (uint *)((int)local_1d0 + 1);
          } while ((int)local_1d0 < 100);
          local_1c8 = (uint *)FUN_007ec0a0(*(undefined4 *)(DAT_00c71678[0x60c0] + 4));
          if (local_1c8 != (uint *)0x0) {
LAB_007620a4:
            FUN_00733ff0(local_1c8,0,0);
          }
          uVar28 = RNG__Next();
          puStack_1d8 = (uint *)FUN_00428b20(5,100,auStack_29c,&DAT_00c7b640,0,local_1c8,uVar28);
          uVar22 = FUN_00732ef0(local_1c8);
          puStack_1d8[0x14c] = uVar22;
          if ((int)uVar11 < 0) {
            uVar11 = FUN_006eed30();
          }
          else {
            puStack_1d8[0x14a] = uVar11;
          }
          local_1cc = (uint *)((int)local_1cc + -1);
        } while (local_1cc != (uint *)0x0);
        local_1cc = (uint *)0x0;
        param_1 = local_1dc;
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      }
      break;
    case 0xb:
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      if ((char)uStack_1c4 != '\0') {
        param_1[0x79d] = 0x708;
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      }
      break;
    case 0x13:
    case 0x14:
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      if ((((char)uStack_1c4 != '\0') &&
          (uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218), param_1[0x79a] != 0)) &&
         (uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218), param_1[0xef] == 0)) {
        local_1cc = (uint *)0x0;
        uStack_34 = 0;
        uStack_2c = 0;
        iVar14 = FUN_0042c7f0();
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        if (0 < iVar14) {
          local_1c0 = (uint *)(iVar14 + -1);
          puVar24 = (uint *)0x0;
          if (-1 < (int)local_1c0) {
            local_1d0 = (uint *)((int)local_1c0 * 0x1c);
            puVar19 = (uint *)0x0;
            do {
              puVar24 = local_1cc;
              if (2 < (int)puVar19) break;
              iVar14 = *(int *)(*(int *)(param_1[0x79a] + 0x1dec) + 8 + (int)local_1d0);
              if (*(char *)(*(int *)(param_1[0x79a] + 0x1dec) + 4 + (int)local_1d0) == '\0') {
                cVar9 = FUN_007ce2a0(iVar14,0);
                if (((cVar9 != '\0') && (piVar21 = (int *)FUN_0072fd10(iVar14), *piVar21 != 3)) &&
                   (0 < *(int *)(*(int *)(param_1[0x79a] + 0x16c8) + iVar14 * 4))) {
                  *(int *)((int)&uStack_34 + (int)local_1cc * 4) = iVar14;
                  local_1cc = (uint *)((int)local_1cc + 1);
                }
              }
              else {
                *(int *)((int)&uStack_34 + (int)puVar19 * 4) = -iVar14;
                local_1cc = (uint *)((int)puVar19 + 1);
              }
              local_1c0 = (uint *)((int)local_1c0 + -1);
              local_1d0 = (uint *)((int)local_1d0 + -0x1c);
              puVar19 = local_1cc;
              puVar24 = local_1cc;
            } while (-1 < (int)local_1c0);
          }
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          local_1d0 = puVar24;
          while (local_1d0 = (uint *)((int)local_1d0 + -1), -1 < (int)local_1d0) {
            iVar14 = *(int *)((int)&uStack_34 + (int)local_1d0 * 4);
            if (iVar14 < 0) {
              uVar11 = -iVar14;
              uStack_31c = 1;
              local_1c0 = (uint *)(uVar11 & 0x7fff);
              uStack_320 = DAT_00c71678[0x993e];
              uStack_318 = uVar11;
              uStack_314 = _DAT_00baaf70;
              uStack_310 = _UNK_00baaf74;
              uStack_30c = _UNK_00baaf78;
              uStack_308 = _UNK_00baaf7c;
              FUN_00721a70(&uStack_320);
              if ((uVar11 & 0x8000) == 0) {
                psVar1 = (short *)(param_1[0x5d2] + (int)local_1c0 * 4);
                *psVar1 = *psVar1 + 1;
              }
              else {
                psVar1 = (short *)(param_1[0x5d2] + 2 + (int)local_1c0 * 4);
                *psVar1 = *psVar1 + 1;
              }
            }
            else if (0 < iVar14) {
              FUN_0075f0e0(iVar14,0,0,0,0,0);
            }
            uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          }
        }
      }
      break;
    case 0x1e:
      param_1[0x7c5] = DAT_00c71678[0x993e] + 1;
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      break;
    case 0x23:
      FUN_007d41d0(0x2ca,2,0);
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      break;
    case 0x24:
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      if ((char)uStack_1c4 != '\0') {
        FUN_00930390(0x7a,0,4);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      }
    }
    break;
  case (uint *)0x26d:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((char)uStack_1c4 != '\0') {
      uVar11 = 0x1518;
      if (1 < (int)DAT_00c71678[0x9985]) {
        uVar11 = 600;
      }
      param_1[0x79d] = uVar11;
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    }
    break;
  case (uint *)0x270:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((char)uStack_1c4 != '\0') {
      puVar24 = param_1 + 0xcf;
      local_1d0 = (uint *)0x0;
      puStack_1d8 = puVar24;
      do {
        if (local_1d0 == (uint *)0x0) {
          uVar28 = RNG__Next();
          uVar29 = 1;
          uVar30 = 0xf;
        }
        else {
          uVar28 = RNG__Next();
          uVar29 = 5;
          uVar30 = 0x19;
        }
        local_1c0 = (uint *)FUN_00734180(uVar28,uVar30,0,uVar29,0);
        FUN_00813520(auStack_2bc,puVar24,0x42200000,0,0,0);
        uVar28 = RNG__Next();
        iVar14 = FUN_00428b20(5,300,auStack_2bc,&DAT_00c7b640,0,local_1c0,uVar28);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        *(uint **)(iVar14 + 0x554) = local_1d0;
        local_1d0 = (uint *)((int)local_1d0 + 1);
        param_1 = local_1dc;
      } while (local_1d0 < (uint *)0x5);
    }
    break;
  case (uint *)0x279:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((char)uStack_1c4 != '\0') {
      iVar14 = FUN_007cae60(0);
      if (0xc < iVar14) {
        iVar14 = 0xc;
      }
      iVar14 = (iVar14 - param_1[0x4d3]) - param_1[0x4d1];
      if (0 < iVar14) {
        FUN_00758a70(iVar14,1,0);
        iVar14 = FUN_007cae60(0);
        if (0xc < iVar14) {
          iVar14 = 0xc;
        }
        iVar14 = (iVar14 - param_1[0x4d3]) - param_1[0x4d1];
        if (0 < iVar14) {
          FUN_00758d00(iVar14,0);
        }
      }
      FUN_009302e0(0x139,1,1);
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    }
    break;
  case (uint *)0x284:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((char)uStack_1c4 == '\0') break;
    afStack_60[7] = (float)param_1[0x55a] * DAT_00baa778 - DAT_00baa630;
    uVar11 = param_1[0x518];
    FUN_009bfc40();
    fVar26 = (float)param_1[0x51c];
    uStack_40 = uVar11;
    FUN_004e4690();
    local_1d0 = (uint *)0xffffffff;
    fStack_3c = fVar26 * _DAT_00baa69c - DAT_00baa630;
    iVar14 = 0;
    fStack_38 = ((float)param_1[0x520] - DAT_00baaac0) / DAT_00baa950 + DAT_00baa630;
    local_1cc = DAT_00baacc4;
    local_1c0 = DAT_00baacc4;
    do {
      puStack_1d8 = local_1c0;
      RNG__Next();
      puVar19 = local_1dc;
      puVar27 = (uint *)((afStack_60[iVar14 + 7] - DAT_00baa06c) +
                        (float)((double)(int)*puVar24 +
                               (double)(&DAT_00bacb00)[-((int)*puVar24 >> 0x1f)]) * DAT_00ba9ff0 *
                        DAT_00baa08c);
      if ((float)puVar27 < (float)local_1c0) {
        local_1c0 = puVar27;
      }
      puVar16 = (uint *)iVar14;
      if ((float)puStack_1d8 <= (float)puVar27) {
        puVar16 = local_1d0;
      }
      iVar14 = iVar14 + 1;
      local_1d0 = puVar16;
    } while (iVar14 < 4);
    switch(puVar16) {
    case (uint *)0x0:
      local_1dc[0x548] = local_1dc[0x548] + 1;
      local_1dc[0x55d] = local_1dc[0x55d] | 0x10;
      break;
    case (uint *)0x1:
      local_1dc[0x549] = local_1dc[0x549] + 1;
      local_1dc[0x55d] = local_1dc[0x55d] | 2;
      break;
    case (uint *)0x2:
      local_1dc[0x54a] = local_1dc[0x54a] + 1;
      local_1dc[0x55d] = local_1dc[0x55d] | 1;
      break;
    case (uint *)0x3:
      local_1dc[0x54b] = local_1dc[0x54b] + 1;
      local_1dc[0x55d] = local_1dc[0x55d] | 8;
    }
    FUN_00763570();
    uVar11 = puVar19[0x4f0];
    afStack_28[0] = (float)(int)puVar19[0x4da];
    afStack_28[1] = (float)(int)puVar19[0x4d7] * DAT_00baa6fc;
    puStack_18 = DAT_00baacc4;
    if (uVar11 == 0x19) {
      afStack_28[3] = 1e+10;
      afStack_28[2] = (float)(int)puVar19[0x7d5] * DAT_00baa6fc;
    }
    else {
      afStack_28[2] = (float)(int)puVar19[0x4d9] * DAT_00baa6fc;
      if (uVar11 == 0x12) {
        afStack_28[3] = ((float)(int)puVar19[0x76a] + (float)(int)puVar19[0x76a]) - DAT_00baa454;
      }
      else {
        afStack_28[3] = 1e+10;
        if (uVar11 == 0x24) {
          puStack_18 = (uint *)(((float)(int)puVar19[0x76b] + (float)(int)puVar19[0x76b]) -
                               DAT_00baa454);
        }
      }
    }
    puVar19 = (uint *)0x0;
    local_1c8 = (uint *)0xffffffff;
    do {
      RNG__Next();
      puVar27 = (uint *)afStack_28[(int)puVar19];
      puVar16 = puVar19;
      if (((float)local_1cc <= (float)puVar27) &&
         (((float)puVar27 != (float)local_1cc || ((*puVar24 & 1) == 0)))) {
        puVar27 = local_1cc;
        puVar16 = local_1c8;
      }
      local_1c8 = puVar16;
      local_1cc = puVar27;
      puVar19 = (uint *)((int)puVar19 + 1);
    } while (puVar19 < &DAT_00000005);
    local_1d0 = (uint *)0x0;
    param_1 = local_1dc;
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    switch(local_1c8) {
    case (uint *)0x0:
      local_1cc = (uint *)&DAT_00000014;
      local_1c8 = (uint *)0x3;
      break;
    case (uint *)0x1:
      local_1cc = (uint *)0x1e;
      local_1c8 = (uint *)0x1;
      break;
    case (uint *)0x2:
      local_1cc = (uint *)0x28;
      local_1c8 = (uint *)0x1;
      break;
    case (uint *)0x3:
      local_1d0 = (uint *)0x3;
      local_1c8 = (uint *)0x1;
      goto LAB_00761cd5;
    case (uint *)0x4:
      local_1d0 = (uint *)0x1;
      local_1c8 = (uint *)0x2;
LAB_00761cd5:
      local_1cc = (uint *)0xa;
      break;
    default:
      goto switchD_00761f55_caseD_2;
    }
    puStack_1d8 = local_1dc + 0xcf;
    iVar14 = 0;
    do {
      uVar28 = RNG__Next();
      uVar30 = FUN_00813520(auStack_350,puStack_1d8,0x42400000,0,0,0);
      iVar23 = FUN_00428b20(5,local_1cc,uVar30,&DAT_00c7b640,0,local_1d0,uVar28);
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      *(int *)(iVar23 + 0x554) = iVar14;
      iVar14 = iVar14 + 1;
      param_1 = local_1dc;
    } while (iVar14 < (int)local_1c8);
    break;
  case (uint *)0x28e:
LAB_00761720:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((char)uStack_1c4 != '\0') {
      FUN_00813520(auStack_2c4,param_1 + 0xcf,0x42200000,0,0,0);
      uVar28 = RNG__Next();
      FUN_00428b20(5,0x46,auStack_2c4,&DAT_00c7b640,param_1,0,uVar28);
      puVar12 = DAT_00c71678;
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      uVar11 = 1;
      do {
        uVar20 = -(uint)((uVar11 & 0x7ff) != 0) & uVar11 & 0x7ff;
        uVar22 = 0xe;
        if (uVar20 < 0xe) {
          uVar22 = uVar20;
        }
        uVar11 = uVar11 + 1;
        *(undefined1 *)((int)puVar12 + uVar22 + 0x1af20) = 1;
      } while (uVar11 < 0xf);
    }
    break;
  case (uint *)0x29c:
    cVar9 = FUN_00827bc0();
    puVar12 = DAT_00c71678;
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if (cVar9 != '\0') {
      cVar9 = FUN_0074f090();
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      if ((cVar9 == '\0') &&
         (uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218), (int)puVar12[0x19de2] < 1)) {
        puVar12[0x19de2] = 1;
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      }
    }
    break;
  case (uint *)0x29f:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((char)uStack_1c4 != '\0') {
      FUN_00813520(auStack_28c,param_1 + 0xcf,0x42200000,0,0,0);
      uVar30 = RNG__Next();
      uVar28 = 1;
      puVar19 = (uint *)0x0;
      puVar13 = auStack_28c;
      iVar14 = 10;
LAB_007627f9:
      FUN_00428b20(5,iVar14,puVar13,&DAT_00c7b640,puVar19,uVar28,uVar30);
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    }
    break;
  case (uint *)0x2ad:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((-1 < (int)local_1d0) &&
       (uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218),
       (int)param_1[(int)local_1d0 * 8 + 0x567] < 2)) {
      param_1[(int)local_1d0 * 8 + 0x567] = 2;
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    }
    break;
  case (uint *)0x2ae:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((char)uStack_1c4 != '\0') {
      FUN_00813520(auStack_294,param_1 + 0xcf,0x42200000,0,0,0);
      uVar30 = RNG__Next();
      uVar28 = 3;
      puVar19 = (uint *)0x0;
      puVar13 = auStack_294;
      iVar14 = 10;
      goto LAB_007627f9;
    }
    break;
  case (uint *)0x2b4:
    FUN_00827bf0(0);
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    break;
  case (uint *)0x2b5:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((char)uStack_1c4 != '\0') {
      iVar14 = 8;
      do {
        FUN_00759bf0(param_1 + 0xcf);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        iVar14 = iVar14 + -1;
      } while (iVar14 != 0);
    }
    break;
  case (uint *)0x2b6:
    iVar14 = FUN_007cafe0();
    if (iVar14 == 3) {
      iVar14 = FUN_007cae60(0);
      iVar23 = 1;
      iVar17 = (iVar14 + -2) / 2;
      bVar25 = SBORROW4(iVar17,1);
      iVar14 = iVar17 + -1;
    }
    else {
      iVar14 = FUN_007cae60(1);
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      if (iVar14 < 9) break;
      iVar14 = FUN_007cae60(0);
      iVar23 = 3;
      iVar17 = (iVar14 + -2) / 2;
      bVar25 = SBORROW4(iVar17,3);
      iVar14 = iVar17 + -3;
    }
    if (bVar25 != iVar14 < 0) {
      iVar23 = iVar17;
    }
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if (0 < iVar23) {
      FUN_007d2a40(iVar23);
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    }
    break;
  case (uint *)0x2cc:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((char)uStack_1c4 != '\0') {
      puStack_1e8 = param_1 + 0xcf;
      FUN_00813520(&uStack_200,puStack_1e8,0x42200000,0,0,0);
      uVar28 = RNG__Next();
      FUN_00428b20(5,0x1e,&uStack_200,&DAT_00c7b640,0,0,uVar28);
      iVar14 = 3;
      do {
        puVar12 = (undefined4 *)FUN_00813520(auStack_360,puStack_1e8,0x42200000,0,0,0);
        uStack_200 = *puVar12;
        uStack_1fc = puVar12[1];
        uVar28 = RNG__Next();
        FUN_00428b20(5,0x14,&uStack_200,&DAT_00c7b640,0,0,uVar28);
        uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
        iVar14 = iVar14 + -1;
        param_1 = local_1dc;
      } while (iVar14 != 0);
    }
    break;
  case (uint *)0x2d1:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((char)uStack_1c4 != '\0') {
      FUN_007e2100(0x3c23d70a);
      FUN_00417510(DAT_00c71678[0x60c0] + 0x1258);
      local_8 = 8;
      local_1d0 = (uint *)0x0;
      if (puStack_204 != (uint *)0x0) {
        do {
          iVar14 = *(int *)(iStack_20c + (int)local_1d0 * 4);
          if (((((1 < (int)DAT_00c71678[0x9985]) && (iVar23 = 1, *(int *)(iVar14 + 0x28) == 1)) ||
               (iVar23 = *(int *)(iVar14 + 0x28), iVar23 - 10U < 0x3de)) &&
              ((*(char *)(iVar14 + 0x173) == '\0' && (iVar23 != 0x21)))) && (iVar23 != 0x11)) {
            *(undefined4 *)(iVar14 + 0x238) = 0;
            FUN_006a8a20();
            FUN_00431310(param_1);
            FUN_006ae280(auStack_404,6000,0,0);
            FUN_00431310(param_1);
            FUN_006ad3c0(auStack_42c,6000,0);
          }
          local_1d0 = (uint *)((int)local_1d0 + 1);
        } while (local_1d0 < puStack_204);
      }
      local_8 = 0xffffffff;
      FUN_004175b0();
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    }
    break;
  case (uint *)0x2dc:
    uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
    if ((char)uStack_1c4 != '\0') {
      local_1c0 = (uint *)0x1;
      puStack_1e8 = (uint *)(*(int *)(DAT_00c7169c + 0x2a42c) - *(int *)(DAT_00c7169c + 0x2a428) >>
                            2);
      uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
      if ((uint *)0x1 < puStack_1e8) {
        do {
          if (((int)local_1c0 < 0) ||
             (*(int *)(DAT_00c7169c + 0x2a42c) - *(int *)(DAT_00c7169c + 0x2a428) >> 2 <=
              (int)local_1c0)) {
            iVar14 = 0;
          }
          else {
            iVar14 = *(int *)(*(int *)(DAT_00c7169c + 0x2a428) + (int)local_1c0 * 4);
          }
          if ((((local_1c0 != (uint *)&DAT_00000037) && (iVar14 != 0)) &&
              (*(int *)(iVar14 + 0x58) == 2)) && (cVar9 = FUN_00730aa0(), cVar9 != '\0')) {
            uVar28 = RNG__Next();
            uVar28 = FUN_00734180(uVar28,0,0xffffffff,0,1);
            FUN_00813520(auStack_2a4,param_1 + 0xcf,0,0,0,0);
            uVar30 = RNG__Next();
            puVar13 = auStack_2a4;
            goto LAB_007627ee;
          }
          uVar8 = CONCAT44(uStack_218._4_4_,(undefined4)uStack_218);
          local_1c0 = (uint *)((int)local_1c0 + 1);
        } while (local_1c0 < puStack_1e8);
      }
    }
  }
switchD_00761f55_caseD_2:
  uStack_218 = uVar8;
  cVar9 = FUN_007706e0(0x298,0);
  if (cVar9 == '\0') {
code_r0x00762861:
    cVar9 = (char)uStack_1c4;
  }
  else {
    cVar10 = FUN_005b1500(0x40000,0);
    cVar9 = (char)uStack_1c4;
    if ((cVar10 != '\0') && (cVar9 != '\0')) {
      uVar11 = param_1[0x79d];
      if ((int)uVar11 < 900) {
        uVar11 = 900;
      }
      param_1[0x79d] = uVar11;
      FUN_00758a70(2,0,0);
      goto code_r0x00762861;
    }
  }
  switch(local_1e0) {
  case (uint *)0xf0:
    if (cVar9 != '\0') {
      iVar14 = 6;
      afStack_60[0] = _DAT_00bab240;
      afStack_60[1] = (float)_UNK_00bab244;
      afStack_60[2] = (float)_UNK_00bab248;
      afStack_60[3] = (float)_UNK_00bab24c;
      afStack_60[4] = 5.60519e-45;
      afStack_60[5] = 7.00649e-45;
      afStack_60[6] = 8.40779e-45;
      do {
        iVar23 = RNG__RandomInt(iVar14 + 1);
        param_1 = local_1dc;
        fVar26 = afStack_60[iVar14];
        afStack_60[iVar14] = afStack_60[iVar23];
        iVar14 = iVar14 + -1;
        afStack_60[iVar23] = fVar26;
      } while (0 < iVar14);
      uVar11 = 0;
      do {
        iVar14 = (-(uint)(uVar11 < 4) & 2) - 1;
        switch(afStack_60[uVar11]) {
        case 0.0:
          if ((param_1[0xb] == 0) &&
             ((2 < (int)(param_1[0x4d3] + param_1[0x762] * 2 + param_1[0x4d0]) || (uVar11 < 4)))) {
            FUN_007588a0(iVar14 * 2,0);
          }
          break;
        case 1.4013e-45:
          param_1[0x548] = param_1[0x548] + iVar14;
          break;
        case 2.8026e-45:
          param_1[0x549] = param_1[0x549] + iVar14;
          break;
        case 4.2039e-45:
          param_1[0x54a] = param_1[0x54a] + iVar14;
          break;
        case 5.60519e-45:
          param_1[0x54b] = param_1[0x54b] + iVar14;
          break;
        case 7.00649e-45:
          param_1[0x54c] = param_1[0x54c] + iVar14;
          break;
        case 8.40779e-45:
          param_1[0x54d] = param_1[0x54d] + iVar14;
        }
        uVar11 = uVar11 + 1;
      } while ((int)uVar11 < 6);
    }
    break;
  case (uint *)0x102:
    if (cVar9 != '\0') {
      if ((param_1[0xb] == 0) && (*(char *)((int)param_1 + 0x20a9) == '\0')) {
        FUN_005b39d0((int)&local_1cc + 2,0x11c,1,0xffffffff,0);
        if ((param_1[0xb] == 0) && (*(char *)((int)param_1 + 0x20a9) == '\0')) {
          FUN_0040ccd0("Glitch",6);
        }
      }
      iVar14 = RNG__RandomInt(3);
      param_1[0x548] = param_1[0x548] + iVar14 + -1;
      iVar14 = RNG__RandomInt(3);
      param_1[0x549] = param_1[0x549] + iVar14 + -1;
      iVar14 = RNG__RandomInt(3);
      param_1[0x54a] = param_1[0x54a] + iVar14 + -1;
      iVar14 = RNG__RandomInt(3);
      param_1[0x54b] = param_1[0x54b] + iVar14 + -1;
      iVar14 = RNG__RandomInt(3);
      param_1[0x54c] = param_1[0x54c] + iVar14 + -1;
      iVar14 = RNG__RandomInt(3);
      param_1[0x55d] = 0xffff;
      param_1[0x54d] = param_1[0x54d] + iVar14 + -1;
    }
    break;
  case (uint *)0x154:
    if (cVar9 != '\0') {
      if (param_1[0xb] != 0) goto LAB_00762c3c;
      uVar28 = RNG__Next();
      uVar30 = FUN_00813520(auStack_328,param_1 + 0xcf,0x42200000,0,0,0);
      FUN_00428b20(5,0x46,uVar30,&DAT_00c7b640,param_1,0,uVar28);
    }
    break;
  case (uint *)0x188:
    uVar28 = FUN_007c7960();
    iVar14 = FUN_0072fd10(uVar28);
    if (iVar14 != 0) {
      param_1[0x55d] = param_1[0x55d] | *(uint *)(iVar14 + 0x54);
    }
    break;
  case (uint *)0x197:
    FUN_005b17c0(0x197);
    uVar11 = RNG__RandomInt(4);
    param_1[0x64b] = uVar11;
    FUN_009302e0(0x197,1,1);
    if ((int)(*(int *)(DAT_00c7169c + 0x2a420) - *(int *)(DAT_00c7169c + 0x2a41c) & 0xfffffffcU) <
        0x45) {
      uVar28 = 0;
    }
    else {
      uVar28 = *(undefined4 *)(*(int *)(DAT_00c7169c + 0x2a41c) + 0x44);
    }
    FUN_0075d1d0(uVar28,0);
    FUN_007c7c60();
    *(undefined2 *)(param_1 + 0xbb2) = 0;
    break;
  case (uint *)0x19f:
    cVar9 = FUN_009305f0(0x19f);
    if (cVar9 == '\0') {
      FUN_009302e0(0x19f,1,1);
      FUN_0040a380("FloatGlow",0);
    }
    break;
  case (uint *)0x1b8:
    param_1[0x643] = DAT_00c71678[0x993e];
    break;
  case (uint *)0x1ba:
    cVar9 = FUN_009305f0(0x1ba);
    if (cVar9 == '\0') {
      FUN_0040a380("FloatNoGlow",0);
    }
  }
switchD_00762884_caseD_f1:
  if ((param_1[0xb] == 0) && ((char)uStack_1c4 != '\0')) {
    uVar11 = 0;
    piVar21 = (int *)(DAT_00c7169c + 0x2a448);
    if (*(int *)(DAT_00c7169c + 0x2a44c) - *piVar21 >> 2 != 0) {
      do {
        if (((-1 < (int)uVar11) && ((int)uVar11 < piVar21[1] - *piVar21 >> 2)) &&
           (iVar14 = *(int *)(*piVar21 + uVar11 * 4), iVar14 != 0)) {
          if (*(int *)(iVar14 + 8) != 0 || *(int *)(iVar14 + 0xc) != 0) {
            cVar9 = FUN_0072fe80(*(int *)(iVar14 + 8),*(int *)(iVar14 + 0xc));
            if (cVar9 != '\0') {
              FUN_0075e320(uVar11,1);
            }
          }
        }
        uVar11 = uVar11 + 1;
        piVar21 = (int *)(DAT_00c7169c + 0x2a448);
      } while (uVar11 < (uint)(*(int *)(DAT_00c7169c + 0x2a44c) - *piVar21 >> 2));
    }
  }
LAB_00762c3c:
  FUN_00763570();
  puVar24 = local_1e0;
  if (((int)local_1e0 < 0) &&
     (((local_1e4[0x16] < 0 || (local_1e4[0x17] < 0)) ||
      ((local_1e4[0x18] < 0 || (local_1e4[0x19] < 0)))))) {
    FUN_007caad0();
  }
  if (*(char *)((int)local_1e4 + 0xb2) == '\0') {
    if ((*local_1e4 == 3) && (param_1[0x580] != 0)) {
      FUN_007ad330(3,0);
    }
  }
  else {
    FUN_0075d1d0(local_1e4,0);
  }
  iVar23 = 0;
  piVar21 = (int *)param_1[0x5b2];
  iVar14 = (int)(param_1[0x5b3] - (int)piVar21) >> 2;
  if (iVar14 != 0) {
    do {
      iVar23 = iVar23 + *piVar21;
      piVar21 = piVar21 + 1;
      iVar14 = iVar14 + -1;
    } while (iVar14 != 0);
    if (0x32 < iVar23) {
      FUN_00929a20(0x14a);
    }
  }
  FUN_007d3200(puVar24 == (uint *)0x248);
  if (*(int *)(DAT_00c7169c + 0x4b3d8) != *(int *)(DAT_00c7169c + 0x4b3dc)) {
    iVar14 = FUN_0090ac70(param_1);
    if (iVar14 != 0) {
      FUN_00425ac0(2,param_1);
    }
  }
  ExceptionList = local_10;
  return;
}
