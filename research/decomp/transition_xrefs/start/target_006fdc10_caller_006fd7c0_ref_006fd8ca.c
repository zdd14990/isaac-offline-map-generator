/* Static decompilation only; PE entry point was not executed. */
/* Target: 006fdc10 */
/* Reference: 006fd8ca */
/* Caller: FUN_006fd7c0 @ 006fd7c0 */


void __thiscall
FUN_006fd7c0(int *param_1,int param_2,undefined4 param_3,uint param_4,int param_5,int param_6)

{
  byte bVar1;
  int *piVar2;
  char cVar3;
  int iVar4;
  int iVar5;
  int *extraout_EDX;
  int *extraout_EDX_00;
  uint uVar6;
  char *pcVar7;
  undefined1 local_5c [40];
  char local_34 [4];
  int local_30;
  uint local_28;
  undefined4 local_24;
  float local_20;
  undefined4 local_1c;
  float local_18;
  int *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;

  local_8 = 0xffffffff;
  puStack_c = &LAB_00afc200;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  local_14 = param_1;
  if (0xbc < param_2 + 0x14U) {
    pcVar7 = "Invalid room index passed to Game::StartRoomTransition()\n";
LAB_006fdbe2:
    Isaac__log(8,pcVar7);
    ExceptionList = local_10;
    return;
  }
  if (0x16 < param_4) {
    pcVar7 = "Invalid animation passed to Game::StartRoomTransition()\n";
    goto LAB_006fdbe2;
  }
  if (2 < param_6) {
    pcVar7 = "Invalid dimension passed to Game::StartRoomTransition()\n";
    goto LAB_006fdbe2;
  }
  if (param_1[0x9985] == 4) {
    param_5 = 0xbb;
LAB_006fd82c:
    FUN_00956780();
    FUN_0092dc30(param_5,0x3f800000,2,0,0x3f800000,0);
    ExceptionList = local_10;
    return;
  }
  if ((((param_4 == 0xc) && (*param_1 == 1)) &&
      (cVar3 = FUN_0074bac0(DAT_00bf93b4 ^ (uint)&stack0xfffffffc), param_1 = extraout_EDX,
      cVar3 == '\0')) &&
     ((extraout_EDX[0x60c1] == extraout_EDX[0x60b4] && (*(char *)(extraout_EDX[0x60c0] + 1) != '\0')
      ))) {
    cVar3 = Level__curse_mode_predicate();
    if (cVar3 == '\0') {
      FUN_006fdc10(0,6,0);
      if (param_5 == 0) {
        ExceptionList = local_10;
        return;
      }
      FUN_007abe20("TeleportUp");
      param_5 = 0xd7;
      goto LAB_006fd82c;
    }
    param_2 = -2;
    param_4 = 3;
    param_1 = local_14;
LAB_006fd8f5:
    param_6 = 0;
  }
  else if (param_2 == -2) goto LAB_006fd8f5;
  if (param_5 == 0) {
    if (param_4 != 3) goto LAB_006fdb29;
LAB_006fdb4d:
    FUN_00705ee0(0xffffffff);
    param_1 = local_14;
  }
  else {
    if ((param_4 == 3) || (param_4 == 0xc)) {
      cVar3 = FUN_008279a0();
      if (cVar3 != '\0') {
        param_6 = 0;
        local_24 = *(undefined4 *)(param_5 + 0x33c);
        local_20 = *(float *)(param_5 + 0x340);
        do {
          FUN_0081e9d0(&local_1c,0);
          if (local_18 <
              ((*(float *)(local_14[0x60c0] + 0x20) - DAT_00baa8d0) - *(float *)(param_5 + 0x370)) -
              DAT_00baa87c) {
            FUN_00945190(&local_1c,&DAT_00c3793c,0);
            FUN_0041ab50(local_34,local_5c,10);
            uVar6 = 0;
            if (local_28 == 0) {
LAB_006fda7d:
              local_24 = local_1c;
              local_20 = local_18;
              FUN_004175b0();
              break;
            }
            while (((((iVar4 = *(int *)(local_30 + uVar6 * 4), *(int *)(DAT_00c71678 + 0x26614) < 2
                      || (iVar5 = 1, *(int *)(iVar4 + 0x28) != 1)) &&
                     (iVar5 = *(int *)(iVar4 + 0x28), 0x3dd < iVar5 - 10U)) ||
                    ((*(uint *)(iVar4 + 0x168) & 0x20000000) != 0)) &&
                   ((iVar5 != 9 || ((*(uint *)(iVar4 + 0x438) & 0x80000000) != 0))))) {
              uVar6 = uVar6 + 1;
              if (local_28 <= uVar6) goto LAB_006fda7d;
            }
            if (local_34[0] == '\0') {
              local_8 = 0;
              FUN_00a648b0(0,0);
              local_8 = 0xffffffff;
            }
          }
          param_6 = param_6 + 1;
        } while (param_6 < 0x32);
        FUN_007cd950(&local_24,1,1);
        iVar4 = *(int *)(param_5 + 0x13bc);
        if (iVar4 < 0x3c) {
          iVar4 = 0x3c;
        }
        *(int *)(param_5 + 0x13bc) = iVar4;
        ExceptionList = local_10;
        return;
      }
      param_1 = extraout_EDX_00;
      if (param_4 == 3) {
        iVar4 = extraout_EDX_00[0x60c0];
        iVar5 = *(int *)(iVar4 + 8);
        if (iVar5 == 0xb) {
          bVar1 = *(byte *)(*(int *)(iVar4 + 4) + 0x44);
joined_r0x006fdafc:
          if ((bVar1 & 1) != 0) goto LAB_006fdb4d;
        }
        else {
          if (iVar5 == 0x11) {
            bVar1 = *(byte *)(*(int *)(iVar4 + 4) + 0x44);
            goto joined_r0x006fdafc;
          }
          if ((iVar5 != 10) && (iVar5 != 3)) goto LAB_006fdb4d;
        }
        FUN_00425ac0(9,param_5);
        goto LAB_006fdb4d;
      }
    }
LAB_006fdb29:
    if (param_4 == 0x10) goto LAB_006fdb4d;
    if ((param_1[0x60c1] == param_1[0x60b4]) && (*(char *)(param_1[0x60c0] + 1) != '\0')) {
      if (param_4 == 0xc) goto LAB_006fdb87;
      goto LAB_006fdb4d;
    }
  }
  if ((param_4 == 0) &&
     (((param_6 < 0 || (param_6 == *(int *)(DAT_00c71678 + 0x1830c))) &&
      (cVar3 = FUN_0074d4a0(param_1[0x60c1],param_2,param_3), cVar3 != '\0')))) {
    param_2 = -0x10;
  }
LAB_006fdb87:
  piVar2 = local_14;
  FUN_0082ee40(param_2,param_3,param_4,param_5,param_6);
  cVar3 = FUN_006f0070();
  if (cVar3 != '\0') {
    piVar2[0x9970] = 0;
  }
  *(undefined1 *)(piVar2 + 0x19dd1) = 0;
  ExceptionList = local_10;
  return;
}
