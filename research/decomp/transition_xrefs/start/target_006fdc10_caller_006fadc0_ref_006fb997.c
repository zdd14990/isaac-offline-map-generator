/* Static decompilation only; PE entry point was not executed. */
/* Target: 006fdc10 */
/* Reference: 006fb997 */
/* Caller: FUN_006fadc0 @ 006fadc0 */


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN_006fadc0(int param_1)

{
  float fVar1;
  ulonglong uVar2;
  longlong lVar3;
  longlong lVar4;
  longlong lVar5;
  char cVar6;
  int iVar7;
  int *piVar8;
  int iVar9;
  float *extraout_ECX;
  int iVar10;
  int *piVar11;
  uint uVar12;
  uint uVar13;
  int *piVar14;
  float fVar15;
  float fVar16;
  ulonglong uVar17;
  undefined4 local_5c;
  undefined4 local_58;
  undefined4 local_54;
  undefined4 uStack_50;
  undefined4 uStack_4c;
  undefined1 auStack_40 [12];
  int local_34;
  undefined **local_30;
  int local_2c;
  undefined4 local_28;
  int *local_24;
  undefined4 local_20;
  uint local_1c;
  int local_18;
  char local_11;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 uStack_8;

  uStack_8 = 0xffffffff;
  puStack_c = &LAB_00afc189;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  local_24 = (int *)0x0;
  local_1c = 0;
  local_18 = param_1;
  cVar6 = FUN_0068bba0(DAT_00bf93b4 ^ (uint)&stack0xfffffffc);
  if (cVar6 != '\0') {
    ExceptionList = local_10;
    return;
  }
  FUN_00708630();
  local_34 = param_1 + 0x1da04;
  FUN_009a2990();
  FUN_004291c0();
  if (0 < *(int *)(param_1 + 0x26528)) {
    *(int *)(param_1 + 0x26528) = *(int *)(param_1 + 0x26528) + -1;
  }
  if ((0 < *(int *)(param_1 + 0x26508)) &&
     (iVar7 = *(int *)(param_1 + 0x26508) + -1, *(int *)(param_1 + 0x26508) = iVar7, iVar7 < 1)) {
    *(undefined4 *)(param_1 + 0x2650c) = DAT_00c7b640;
    *(undefined4 *)(param_1 + 0x26510) = DAT_00c7b644;
  }
  if (0 < *(int *)(param_1 + 0x26538)) {
    *(int *)(param_1 + 0x26538) = *(int *)(param_1 + 0x26538) + -1;
  }
  if (((((*(char *)(param_1 + 0x676b4) != '\0') &&
        (FUN_006ef410((float *)(param_1 + 0x676d0),param_1 + 0x676e8),
        *extraout_ECX == *(float *)(param_1 + 0x676d0))) &&
       (extraout_ECX[1] == *(float *)(param_1 + 0x676d4))) &&
      ((extraout_ECX[2] == *(float *)(param_1 + 0x676d8) &&
       (extraout_ECX[3] == *(float *)(param_1 + 0x676dc))))) &&
     ((extraout_ECX[4] == *(float *)(param_1 + 0x676e0) &&
      (extraout_ECX[5] == *(float *)(param_1 + 0x676e4))))) {
    *(undefined1 *)(param_1 + 0x676b4) = 0;
  }
  fVar15 = *(float *)(param_1 + 0x67734);
  if (0.0 < fVar15) {
    if (fVar15 <= DAT_00baa0d0) {
      *(undefined4 *)(param_1 + 0x67734) = 0;
    }
    else {
      *(float *)(param_1 + 0x67734) = fVar15 * DAT_00baa380;
    }
  }
  fVar15 = *(float *)(param_1 + 0x265b0);
  if (fVar15 <= 0.0) goto LAB_006fb3bd;
  if (*(int *)(param_1 + 0x265bc) == 0) {
    fVar15 = fVar15 - *(float *)(param_1 + 0x265b8);
    *(float *)(param_1 + 0x265b0) = fVar15;
    if (fVar15 < 0.0) {
      *(undefined4 *)(param_1 + 0x265b0) = 0;
    }
    goto LAB_006fb3b6;
  }
  fVar15 = *(float *)(param_1 + 0x265b8) + fVar15;
  *(float *)(param_1 + 0x265b0) = fVar15;
  if (*(int *)(param_1 + 0x22ed4) != 2) {
    *(undefined4 *)(param_1 + 0x22ed4) = 1;
    *(undefined4 *)(param_1 + 0x22edc) = 2;
  }
  if (fVar15 < DAT_00baa454) goto LAB_006fb3b6;
  *(undefined4 *)(param_1 + 0x265b0) = 0x3f800000;
  switch(*(int *)(param_1 + 0x265bc)) {
  case 1:
    FUN_00a0f550(0xff000000);
    iVar7 = DAT_00c7169c;
    *(undefined4 *)(DAT_00c7169c + 0x4b28c) = 2;
    goto LAB_006fb36f;
  case 2:
LAB_006fafdc:
    FUN_00a0f550(0xff000000);
    iVar7 = DAT_00c7169c;
    *(undefined4 *)(DAT_00c7169c + 0x4b28c) = 3;
    goto LAB_006fb36f;
  case 3:
    FUN_00a0f550(0xff000000);
    iVar7 = DAT_00c7169c;
    *(undefined4 *)(DAT_00c7169c + 0x4b28c) = 0x13;
    goto LAB_006fb36f;
  case 4:
    FUN_00a0f550(0xff000000);
    iVar7 = DAT_00c7169c;
    *(undefined4 *)(DAT_00c7169c + 0x4b28c) = 1;
    goto LAB_006fb36f;
  case 5:
    iVar7 = PlayerManager__get_player_417870(0);
    if ((*(int *)(iVar7 + 0x13c0) == 9) ||
       (iVar7 = PlayerManager__get_player_417870(0), *(int *)(iVar7 + 0x13c0) == 0x1e)) {
      if (*(int *)(DAT_00c7169c + 0x324) == 0) goto LAB_006fafdc;
      FUN_00929b40(0x15,0xffffffff);
LAB_006fb0d4:
      FUN_009e9320(DAT_00c71678 + 0x1bb84);
      FUN_00958cb0();
    }
    else {
      FUN_009e9320(DAT_00c71678 + 0x1bb84);
      FUN_00958cb0();
    }
    break;
  case 6:
    if (*(int *)(DAT_00c7169c + 0x4b3d8) == *(int *)(DAT_00c7169c + 0x4b3dc)) {
LAB_006fb16a:
      local_11 = '\x01';
    }
    else {
      FUN_00a29f60(auStack_40);
      uStack_8 = 0;
      local_1c = 1;
      piVar8 = (int *)FUN_00a286f0(&local_30);
      uStack_8 = 1;
      local_24 = (int *)0x3;
      local_1c = 3;
      cVar6 = (**(code **)(*piVar8 + 0x14))();
      if ((cVar6 != '\0') && (cVar6 = FUN_0090c400(), cVar6 != '\0')) goto LAB_006fb16a;
      local_11 = '\0';
    }
    piVar8 = local_24;
    if (((uint)local_24 & 2) != 0) {
      piVar8 = (int *)((uint)local_24 & 0xfffffffd);
      local_30 = KAGE::System::UserProfileBase::vftable;
    }
    uStack_8 = 0xffffffff;
    if (((uint)piVar8 & 1) != 0) {
      FUN_008e24c0();
    }
    if (local_11 != '\0') {
      iVar7 = FUN_009b92c0(0);
      iVar7 = *(int *)(iVar7 + 0x13c0);
      local_24 = *(int **)(DAT_00c7169c + 0x324);
      FUN_00929b40(0x16,-*(int *)(DAT_00c7169c + 0x328));
      if (((iVar7 == 9) || (iVar7 == 0x1e)) && (local_24 != (int *)0x0)) {
        FUN_00929b40(0x15,0xffffffff);
      }
      if (*(int *)(DAT_00c7169c + 0x4b3d8) != *(int *)(DAT_00c7169c + 0x4b3dc)) {
        FUN_0090c560();
      }
      goto LAB_006fb0d4;
    }
    FUN_0090df40(0);
    break;
  case 7:
    FUN_006f7ac0();
    break;
  case 8:
    FUN_00a29f60(auStack_40);
    uStack_8 = 2;
    local_1c = 4;
    piVar8 = (int *)FUN_00a286f0(&local_30);
    uStack_8 = 3;
    local_1c = 0xc;
    cVar6 = (**(code **)(*piVar8 + 0x14))();
    if (cVar6 == '\0') {
LAB_006fb28b:
      local_11 = '\0';
    }
    else {
      cVar6 = FUN_0090c400();
      local_11 = '\x01';
      if (cVar6 == '\0') goto LAB_006fb28b;
    }
    local_30 = KAGE::System::UserProfileBase::vftable;
    uStack_8 = 0xffffffff;
    FUN_008e24c0();
    iVar7 = DAT_00c7169c;
    if (local_11 != '\0') {
      local_1c = 0;
      iVar10 = *(int *)(DAT_00c7169c + 0x4b27c) - *(int *)(DAT_00c7169c + 0x4b278);
      iVar9 = iVar10 >> 0x1f;
      if (iVar10 / 0x14 + iVar9 != iVar9) {
        iVar9 = 0;
        do {
          local_1c = local_1c + 1;
          *(byte *)(iVar9 + 8 + *(int *)(iVar7 + 0x4b278)) =
               *(byte *)(iVar9 + 8 + *(int *)(iVar7 + 0x4b278)) | 1;
          iVar9 = iVar9 + 0x14;
          param_1 = local_18;
        } while (local_1c < (uint)((*(int *)(iVar7 + 0x4b27c) - *(int *)(iVar7 + 0x4b278)) / 0x14));
      }
      FUN_0090c560();
      FUN_0090df40(1);
    }
    break;
  case 10:
    FUN_00429570();
    break;
  case 0xb:
    FUN_00a0f550(0xff000000);
    iVar7 = DAT_00c7169c;
    *(undefined4 *)(DAT_00c7169c + 0x4b28c) = 0x11;
LAB_006fb36f:
    *(undefined4 *)(iVar7 + 0x4b290) = local_5c;
    *(undefined4 *)(iVar7 + 0x4b294) = local_58;
    *(undefined4 *)(iVar7 + 0x4b298) = local_54;
    *(undefined4 *)(iVar7 + 0x4b29c) = uStack_50;
    *(undefined1 *)(iVar7 + 0x4b288) = 1;
    *(undefined4 *)(iVar7 + 0x4b2a0) = uStack_4c;
  }
  *(undefined1 *)(DAT_00c7169c + 0x29fb8) = 0;
  if ((*(int *)(param_1 + 0x265bc) != 8) && (*(int *)(param_1 + 0x265bc) != 9)) {
    *(undefined4 *)(param_1 + 0x265bc) = 0;
  }
LAB_006fb3b6:
  FUN_009a2b30();
LAB_006fb3bd:
  if (0 < *(int *)(param_1 + 0x264f4)) {
    *(int *)(param_1 + 0x264f4) = *(int *)(param_1 + 0x264f4) + -1;
    FUN_009a2b30();
    ExceptionList = local_10;
    return;
  }
  if (*(int *)(param_1 + 0x1d520) != 0) {
    if (*(char *)(param_1 + 0x1d63c) != '\0') {
      FUN_0092e300();
      *(undefined1 *)(param_1 + 0x1d63c) = 0;
    }
    piVar8 = DAT_00c7987c;
    if (*(int *)(DAT_00c7169c + 0x4b3d8) != *(int *)(DAT_00c7169c + 0x4b3dc)) {
      piVar11 = (int *)0x0;
      local_24 = (int *)*DAT_00c7987c;
      piVar14 = local_24;
      if (local_24 != DAT_00c7987c) {
        piVar14 = (int *)0x0;
        do {
          piVar11 = (int *)((int)piVar14 + 1);
          if (local_24[6] != 0) {
            piVar11 = piVar14;
          }
          std::
          _Tree_unchecked_const_iterator<std::_Tree_val<std::_Tree_simple_types<unsigned_int>_>,std::_Iterator_base0>
          ::operator++((_Tree_unchecked_const_iterator<std::_Tree_val<std::_Tree_simple_types<unsigned_int>_>,std::_Iterator_base0>
                        *)&local_24);
          param_1 = local_18;
          piVar14 = piVar11;
        } while (local_24 != piVar8);
      }
      local_24 = piVar14;
      *(bool *)(DAT_00c7169c + 0x4aba0) = piVar11 == (int *)0x0;
    }
    FUN_009b6840();
    if (*(int *)(param_1 + 0x24ecc) == 0) {
      ExceptionList = local_10;
      return;
    }
    *(undefined4 *)(param_1 + 0x24ecc) = 2;
    *(undefined4 *)(param_1 + 0x24ed8) = 8;
    *(undefined4 *)(param_1 + 0x24ed0) = 0xffffffff;
    ExceptionList = local_10;
    return;
  }
  if (*(int *)(param_1 + 0x1d654) != 0) {
    FUN_00857450();
    ExceptionList = local_10;
    return;
  }
  if (*(int *)(param_1 + 0x1ba78) != 0) {
    FUN_0092f1c0();
    FUN_009a2b30();
    ExceptionList = local_10;
    return;
  }
  if (*(int *)(param_1 + 0x1b83c) != 0) {
    FUN_008318a0();
    FUN_0098dba0();
    FUN_009a2b30();
    cVar6 = FUN_006f0070();
    if (cVar6 == '\0') {
      ExceptionList = local_10;
      return;
    }
    *(undefined4 *)(param_1 + 0x265c0) = 0;
    ExceptionList = local_10;
    return;
  }
  if (*(int *)(param_1 + 0x1c034) == 0) {
    cVar6 = FUN_00838210();
    if (cVar6 != '\0') {
      FUN_00837ab0(0);
      if (*(char *)(param_1 + 0x268a8) != '\0') {
        ExceptionList = local_10;
        return;
      }
      if (*(int *)(param_1 + 0x268a4) != 1) {
        ExceptionList = local_10;
        return;
      }
      FUN_00a0f550(0xff000000);
      *(undefined4 *)(param_1 + 0x265b8) = 0x3da3d70a;
      *(undefined4 *)(param_1 + 0x265bc) = 7;
      *(undefined4 *)(param_1 + 0x265a4) = local_5c;
      *(undefined4 *)(param_1 + 0x265a8) = local_58;
      *(undefined4 *)(param_1 + 0x265ac) = local_54;
      *(undefined4 *)(param_1 + 0x265b0) = *(undefined4 *)(param_1 + 0x265b0);
      *(undefined4 *)(param_1 + 0x265b4) = 0;
      *(float *)(param_1 + 0x265b0) = *(float *)(param_1 + 0x265b0) + DAT_00baa108;
      ExceptionList = local_10;
      return;
    }
    if (*(char *)(param_1 + 0x25954) != '\0') {
      ExceptionList = local_10;
      return;
    }
  }
  else {
    local_24 = (int *)(param_1 + 0x23a74);
    if (((*(int *)(param_1 + 0x23a74) == 0) ||
        (*(int *)(DAT_00c7169c + 0x4b3d8) != *(int *)(DAT_00c7169c + 0x4b3dc))) &&
       (FUN_009aca90(0), *(int *)(param_1 + 0x1c034) == 2)) {
      FUN_009a2b30();
      if (*local_24 == 0) {
        ExceptionList = local_10;
        return;
      }
      FUN_009b6840();
      ExceptionList = local_10;
      return;
    }
  }
  local_11 = *(char *)(param_1 + 0x269e8);
  iVar7 = DAT_00c7169c;
  if (0.0 < *(float *)(param_1 + 0x26598)) {
    if ((*(int *)(DAT_00c7169c + 0x4b3d8) == *(int *)(DAT_00c7169c + 0x4b3dc)) && (local_11 == '\0')
       ) {
      uVar17 = FUN_00a68490();
      uVar12 = (uint)(uVar17 >> 0x20);
      uVar2 = (uVar17 & 0xffffffff) * 0xd7b634db;
      local_30 = (undefined **)uVar2;
      lVar3 = (uVar17 & 0xffffffff) * 0x431bde82;
      local_28 = (undefined4)((ulonglong)lVar3 >> 0x20);
      lVar4 = (ulonglong)uVar12 * 0xd7b634db;
      local_1c = (uint)((ulonglong)lVar4 >> 0x20);
      lVar5 = (ulonglong)uVar12 * 0x431bde82;
      local_24 = (int *)lVar5;
      uVar2 = lVar4 + (uVar2 >> 0x20);
      uVar13 = (uint)(uVar2 >> 0x20);
      lVar3 = lVar3 + (uVar2 & 0xffffffff);
      local_20 = (undefined4)lVar3;
      uVar12 = (uint)((ulonglong)lVar3 >> 0x20);
      lVar5 = lVar5 + (ulonglong)CONCAT14(CARRY4(uVar13,uVar12),uVar13 + uVar12);
      uVar12 = (uint)((ulonglong)lVar5 >> 0x20);
      uVar13 = (uint)lVar5 >> 0x12 | uVar12 * 0x4000;
      local_2c = ((uVar12 >> 0x12) - *(int *)(DAT_00c7169c + 0x4ae24)) -
                 (uint)(uVar13 < *(uint *)(DAT_00c7169c + 0x4ae20));
      param_1 = local_18;
      if ((local_2c == 0) &&
         (iVar7 = DAT_00c7169c, uVar13 - *(uint *)(DAT_00c7169c + 0x4ae20) < 0xbb9))
      goto LAB_006fb811;
    }
    iVar7 = DAT_00c7169c;
    fVar15 = *(float *)(param_1 + 0x26598) - *(float *)(param_1 + 0x265b8);
    *(float *)(param_1 + 0x26598) = fVar15;
    *(undefined4 *)(param_1 + 0x22ed4) = 2;
    *(undefined4 *)(param_1 + 0x22edc) = 2;
    if ((fVar15 <= 0.0) || (local_11 != '\0')) {
      *(undefined1 *)(param_1 + 0x269e8) = 0;
      *(undefined4 *)(param_1 + 0x26598) = 0;
      if (*(int *)(param_1 + 0x26614) < 2) {
        FUN_00746560(0);
        FUN_009bea10(1);
      }
      FUN_0040c7f0(0);
      FUN_0040c7f0(0);
      iVar7 = DAT_00c7169c;
    }
  }
LAB_006fb811:
  if (0.0 < *(float *)(param_1 + 0x26598)) {
    FUN_009a2b30();
    ExceptionList = local_10;
    return;
  }
  if ((((*(char *)(iVar7 + 0x4b3ca) == '\0') && (*(char *)(iVar7 + 0x2a3a5) != '\0')) &&
      (*(int *)(iVar7 + 0x4b3d8) == *(int *)(iVar7 + 0x4b3dc))) &&
     (*(int *)(param_1 + 0x23a74) == 0)) {
    FUN_009b7680();
    iVar7 = DAT_00c7169c;
  }
  local_2c = param_1 + 0x23a74;
  if (*(int *)(param_1 + 0x23a74) != 0) {
    FUN_009b6840();
    iVar7 = *(int *)(param_1 + 0x18300);
    iVar9 = *(int *)(iVar7 + 0x12f8);
    local_34 = iVar7;
    FUN_0041d030(iVar7 + 0x12f8,*(undefined4 *)(iVar9 + 4));
    *(int *)(iVar9 + 4) = iVar9;
    *(int *)iVar9 = iVar9;
    *(int *)(iVar9 + 8) = iVar9;
    *(undefined4 *)(iVar7 + 0x12fc) = 0;
    *(undefined4 *)(local_34 + 0x12a4) = 0;
    cVar6 = FUN_009b7650();
    iVar7 = DAT_00c7169c;
    param_1 = local_18;
    if (cVar6 != '\0') {
      ExceptionList = local_10;
      return;
    }
  }
  if ((*(int *)(iVar7 + 0x4b3d8) == *(int *)(iVar7 + 0x4b3dc)) && (*(int *)(param_1 + 0x24ecc) != 0)
     ) {
    FUN_008ef990();
    ExceptionList = local_10;
    return;
  }
  *(int *)(param_1 + 0x265c0) = *(int *)(param_1 + 0x265c0) + 1;
  FUN_0098dba0();
  FUN_004212c0();
  if (0 < *(int *)(param_1 + 0x67788)) {
    iVar7 = *(int *)(param_1 + 0x67788) + 1;
    *(int *)(param_1 + 0x67788) = iVar7;
    *(int *)(param_1 + 0x26508) = iVar7 / 6 + 2;
    if (0x59 < iVar7) {
      *(undefined4 *)(param_1 + 0x26508) = 0;
      *(undefined4 *)(param_1 + 0x67788) = 0;
      *(undefined4 *)(param_1 + 0x2650c) = DAT_00c7b640;
      *(undefined4 *)(param_1 + 0x26510) = DAT_00c7b644;
      FUN_006fdc10(0,5,0);
    }
  }
  if (0 < *(int *)(param_1 + 0x68d6c)) {
    iVar9 = *(int *)(param_1 + 0x68d6c) + -1;
    *(undefined4 *)(param_1 + 0x26508) = 10;
    *(int *)(param_1 + 0x68d6c) = iVar9;
    iVar7 = DAT_00c71678;
    if ((iVar9 < 1) && (*(undefined4 *)(param_1 + 0x68d6c) = 0, *(int *)(iVar7 + 0x1830c) == 2)) {
      *(undefined4 *)(iVar7 + 0x18318) = 0xffffffff;
      FUN_006fd7c0(*(undefined4 *)(iVar7 + 0x18900),0xffffffff,0x14,0,
                   (int)*(char *)(iVar7 + 0x18904));
    }
  }
  *(int *)(param_1 + 0x264fc) = *(int *)(param_1 + 0x264fc) + 1;
  iVar7 = *(int *)(param_1 + 0x264f8) + 1;
  *(int *)(param_1 + 0x264f8) = iVar7;
  if ((iVar7 == (iVar7 / 0x1e) * 0x1e) && (*(int *)(param_1 + 0x22ed4) != 2)) {
    *(undefined4 *)(param_1 + 0x22ed4) = 1;
    *(undefined4 *)(param_1 + 0x22edc) = 2;
  }
  FUN_00802980();
  FUN_009bb5d0();
  FUN_004257b0();
  fVar15 = DAT_00baa454;
  if (*(int *)(param_1 + 0x26514) < 1) {
    fVar15 = *(float *)(param_1 + 0x26518) - DAT_00baa0b4;
    *(float *)(param_1 + 0x26518) = fVar15;
    if (fVar15 < 0.0) {
      *(undefined4 *)(param_1 + 0x26518) = 0;
    }
  }
  else {
    fVar16 = *(float *)(param_1 + 0x26518) + _DAT_00baa0c4;
    *(float *)(param_1 + 0x26518) = fVar16;
    if (fVar15 < fVar16) {
      *(undefined4 *)(param_1 + 0x26518) = 0x3f800000;
    }
    *(int *)(param_1 + 0x26514) = *(int *)(param_1 + 0x26514) + -1;
  }
  fVar15 = *(float *)(param_1 + 0x67738);
  fVar16 = *(float *)(param_1 + 0x6773c);
  if (fVar15 != fVar16) {
    fVar1 = *(float *)(param_1 + 0x67740);
    if (fVar1 < (float)((uint)(fVar15 - fVar16) & DAT_00bacb40)) {
      if (fVar16 <= fVar15) {
        fVar16 = fVar15 - fVar1;
      }
      else {
        fVar16 = fVar1 + fVar15;
      }
    }
    *(float *)(param_1 + 0x67738) = fVar16;
  }
  if (0 < *(int *)(param_1 + 0x269e0)) {
    *(int *)(param_1 + 0x269e0) = *(int *)(param_1 + 0x269e0) + -1;
  }
  FUN_009a2b30();
  if ((*(int *)(param_1 + 0x67730) != 0) &&
     (piVar8 = (int *)**(int **)(param_1 + 0x6772c), piVar8 != *(int **)(param_1 + 0x6772c))) {
    do {
      iVar7 = piVar8[3];
      if (iVar7 == 0) {
        piVar11 = (int *)*piVar8;
        *(int **)piVar8[1] = piVar11;
        *(int *)(*piVar8 + 4) = piVar8[1];
        *(int *)(local_18 + 0x67730) = *(int *)(local_18 + 0x67730) + -1;
        FUN_004147f0();
        FUN_00426980();
        FID_conflict__Tidy();
        FUN_0042f240();
        FUN_00aef15c(piVar8,0x40);
        param_1 = local_18;
      }
      else {
        if (0 < iVar7) {
          piVar8[3] = iVar7 + -1;
        }
        piVar11 = (int *)*piVar8;
      }
      piVar8 = piVar11;
    } while (piVar11 != *(int **)(param_1 + 0x6772c));
  }
  FUN_008607a0();
  ExceptionList = local_10;
  return;
}
