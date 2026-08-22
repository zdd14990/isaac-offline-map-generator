/* Static decompilation only; PE entry point was not executed. */
/* Target: 006fdc10 */
/* Reference: 008946f8 */
/* Caller: FUN_008946e0 @ 008946e0 */


undefined4 * __fastcall FUN_008946e0(undefined4 *param_1)

{
  undefined4 uVar1;
  undefined4 *puVar2;
  undefined4 uVar3;

  uVar1 = *param_1;
  puVar2 = (undefined4 *)lua_newuserdata(uVar1,4);
  *puVar2 = FUN_006fdc10;
  lua_pushcclosure(uVar1,FUN_008b8bb0,1);
  uVar3 = lua_absindex(uVar1,0xfffffffd);
  lua_pushstring(uVar1,"StartStageTransition");
  lua_rotate(uVar1,0xfffffffe,1);
  lua_rawset(uVar1,uVar3);
  return param_1;
}
