/* Static decompilation only; PE entry point was not executed. */
/* Target: 006fdc10 */
/* Reference: 005c7bde */
/* Caller: FUN_005c7ad0 @ 005c7ad0 */


void FUN_005c7ad0(int param_1)

{
  int iVar1;
  code *pcVar2;
  uint uVar3;
  uint uVar4;

  iVar1 = *(int *)(param_1 + 0x3bc);
  if ((iVar1 != 0) && (*(int *)(iVar1 + 0x28) == 1)) {
    FUN_00956780();
    FUN_0092dc30(0x41e,0x3f800000,2,0,0x3f800000,0);
    FUN_007abe20("Appear");
    if ((DAT_00c71678[1] == 4) || (DAT_00c71678[1] == 5)) {
      uVar4 = *DAT_00c71678 + 1;
    }
    else {
      uVar4 = *DAT_00c71678;
    }
    uVar4 = -(uint)(uVar4 != 0) & uVar4;
    uVar3 = 0xd;
    if (uVar4 < 0xd) {
      uVar3 = uVar4;
    }
    uVar4 = DAT_00c71678[uVar3 + 0x6ee7];
    if (uVar4 == 0) {
      Isaac__log(0x10,"RNG Seed is zero!\n");
      pcVar2 = (code *)swi(3);
      (*pcVar2)();
      return;
    }
    uVar4 = uVar4 >> ((byte)DAT_00b1f69c & 0x1f) ^ uVar4;
    uVar4 = uVar4 << ((byte)((ulonglong)DAT_00b1f69c >> 0x20) & 0x1f) ^ uVar4;
    DAT_00c71678[uVar3 + 0x6ee7] = uVar4 >> ((byte)DAT_00b1f6a4 & 0x1f) ^ uVar4;
    FUN_006fdc10(1,1,iVar1);
  }
  return;
}
