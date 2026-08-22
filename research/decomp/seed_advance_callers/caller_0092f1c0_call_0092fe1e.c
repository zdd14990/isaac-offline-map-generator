/* Static decompilation only; PE entry point was not executed. */
/* Caller: FUN_0092f1c0 @ 0092f1c0 */
/* advance_stage_slot call site: 0092fe1e */


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0092f1c0(int *param_1)

{
  int *piVar1;
  int iVar2;
  uint uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  int *piVar6;
  int *piVar7;
  int iVar8;
  int iVar9;
  uint uVar10;
  char cVar11;
  bool bVar12;
  float fVar13;
  double dVar14;
  float local_68;
  float local_64;
  float local_60;
  float local_5c;
  float local_58;
  float local_54;
  float local_50;
  int *local_4c;
  int *local_48;
  int local_44;
  int local_40;
  char local_39;
  int *local_38;
  int *local_34;
  char local_2e;
  char local_2d;
  uint local_2c;
  undefined4 local_1c;
  uint local_18;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;

  local_8 = 0xffffffff;
  puStack_c = &LAB_00b0aced;
  local_10 = ExceptionList;
  local_14 = DAT_00bf93b4 ^ (uint)&stack0xfffffffc;
  ExceptionList = &local_10;
  local_4c = param_1;
  switch(*param_1) {
  case 1:
    local_2d = '\x01';
    local_48 = (int *)0x0;
    local_34 = (int *)0x0;
    local_40 = 1000;
    local_2e = '\0';
    FUN_004186c0();
    if (((param_1[4] == 4) && (*(float *)(DAT_00c71678[0x6edc] + 0x1b1c) == DAT_00c7b640)) &&
       (*(float *)(DAT_00c71678[0x6edc] + 0x1b20) == DAT_00c7b644)) {
      piVar6 = (int *)DAT_00c71678[0x6eaa];
      if (piVar6 != (int *)DAT_00c71678[0x6eab]) {
        do {
          piVar7 = (int *)*piVar6;
          if ((piVar7 != (int *)0x0) && (piVar7[0xb] == 0)) {
            (**(code **)(*piVar7 + 0xc))();
          }
          piVar6 = piVar6 + 1;
        } while (piVar6 != (int *)DAT_00c71678[0x6eab]);
      }
      break;
    }
    piVar6 = (int *)DAT_00c71678[0x6eaa];
    piVar7 = (int *)0x0;
    if (piVar6 != (int *)DAT_00c71678[0x6eab]) {
      do {
        piVar7 = (int *)*piVar6;
        if ((piVar7 != (int *)0x0) && (piVar7[0xb] == 0)) {
          if ((char)piVar7[0x4e6] == '\0') {
LAB_0092f31d:
            local_39 = '\0';
          }
          else {
            if (piVar7[0x1f] != 0) {
              local_38 = (int *)piVar7[0x22];
              dVar14 = floor((double)(float)local_38);
              local_38 = (int *)(float)dVar14;
              if ((int)dVar14 != *(int *)(piVar7[0x1f] + 0x30) + -1) goto LAB_0092f31d;
            }
            local_39 = '\x01';
          }
          (**(code **)(*piVar7 + 0xc))();
          if ((*(char *)((int)piVar7 + 0x173) == '\0') && (param_1[4] != 1)) {
            if ((((char)piVar7[0x4e6] == '\0') && (*(char *)((int)piVar7 + 0x139a) == '\0')) ||
               ((*(char *)((int)piVar7 + 0x20a9) != '\0' &&
                (((float)piVar7[0x6c8] - (float)piVar7[0xd0]) *
                 ((float)piVar7[0x6c8] - (float)piVar7[0xd0]) +
                 ((float)piVar7[0x6c7] - (float)piVar7[0xcf]) *
                 ((float)piVar7[0x6c7] - (float)piVar7[0xcf]) <= DAT_00baa454)))) {
              if (local_39 == '\0') {
                if ((*(char *)((int)piVar7 + 0x171) != '\0') && (local_48 == (int *)0x0)) {
                  local_48 = piVar7;
                }
              }
              else {
                *(undefined1 *)((int)piVar7 + 0x171) = 0;
              }
            }
            else {
              local_2d = '\0';
              if (piVar7[0x1f] == 0) {
                iVar8 = -1;
              }
              else {
                local_38 = (int *)piVar7[0x22];
                dVar14 = floor((double)(float)local_38);
                iVar8 = (int)dVar14;
              }
              local_38 = piVar7;
              if (local_40 <= iVar8) {
                iVar8 = local_40;
                local_38 = local_34;
              }
              local_40 = iVar8;
              local_34 = local_38;
              FUN_0092f050(piVar7,0);
              if ((piVar7[0x1f] != 0) && (cVar11 = FUN_0040add0(), cVar11 != '\0')) {
                local_2e = '\x01';
                local_34 = local_38;
              }
            }
          }
        }
        piVar6 = piVar6 + 1;
      } while (piVar6 != (int *)DAT_00c71678[0x6eab]);
      piVar7 = local_34;
      if (local_34 != (int *)0x0) {
        iVar8 = local_34[0x6c8];
        param_1[6] = local_34[0x6c7];
        param_1[7] = iVar8;
      }
    }
    iVar8 = DAT_00c71678[0x60c0];
    iVar9 = (int)(((float)param_1[6] - DAT_00baa904) / DAT_00baa904 + DAT_00baa2d0);
    iVar2 = (int)(((float)param_1[7] - DAT_00baaa00) / DAT_00baa904 + DAT_00baa2d0);
    cVar11 = local_2d;
    if ((((-1 < iVar9) && (iVar9 < *(int *)(iVar8 + 0xc))) && (-1 < iVar2)) &&
       (((iVar2 < *(int *)(iVar8 + 0x10) &&
         (uVar3 = iVar2 * *(int *)(iVar8 + 0xc) + iVar9, uVar3 < 0x1c0)) &&
        ((iVar8 = *(int *)(iVar8 + 0x24 + uVar3 * 4), local_44 = iVar8, iVar8 != 0 &&
         ((*(int *)(iVar8 + 4) == 0x11 && (*(int *)(iVar8 + 8) == 0)))))))) {
      if (local_2e != '\0') {
        cVar11 = FUN_0040a5d0("Player Exit",1);
        if (cVar11 != '\0') {
          FUN_0040a1b0();
          *(undefined1 *)(iVar8 + 0x84) = 1;
        }
        if (*(float *)(DAT_00c71678[0x60c0] + 0x7240) <= DAT_00baa198) {
          uVar4 = FUN_006eef60();
          uVar5 = FUN_00709df0();
          piVar6 = (int *)FUN_00428b20(1000,0xf,uVar5,&DAT_00c7b640,0,2,uVar4);
          piVar6[0x5b] = piVar6[0x5b] | 0x1000;
          piVar6[0x5a] = piVar6[0x5a];
          piVar6[0x3f] = 0x3f000000;
          piVar6[0x53] = 0x40000000;
          piVar6[0xd6] = 0x40800000;
          (**(code **)(*piVar6 + 0xc))();
        }
        else {
          uVar4 = FUN_006eef60();
          uVar5 = FUN_00709df0();
          piVar6 = (int *)FUN_00428b20(1000,99,uVar5,&DAT_00c7b640,0,0,uVar4);
          piVar6[0x5b] = piVar6[0x5b] | 0x1000;
          piVar6[0x5a] = piVar6[0x5a];
          piVar6[0x39] = (int)((float)piVar6[0x39] + (float)piVar6[0x39]);
          piVar6[0x3a] = (int)((float)piVar6[0x3a] + (float)piVar6[0x3a]);
          piVar6[0x53] = 0x40000000;
          (**(code **)(*piVar6 + 0xc))();
          uVar3 = FUN_006eef60();
          iVar8 = local_44;
          local_38 = (int *)(uVar3 % 5 + 3);
          if (local_38 != (int *)0x0) {
            do {
              uVar4 = FUN_006eef60();
              iVar2 = FUN_006eef60();
              fVar13 = (float)((double)iVar2 + (double)(&DAT_00bacb00)[-(iVar2 >> 0x1f)]) *
                       DAT_00ba9ff4 * DAT_00baa704;
              fVar13 = fVar13 + fVar13;
              local_58 = fVar13;
              FUN_0041d520();
              local_60 = fVar13;
              iVar2 = FUN_006eef60();
              local_5c = (float)((double)iVar2 + (double)(&DAT_00bacb00)[-(iVar2 >> 0x1f)]) *
                         DAT_00ba9ff4 * DAT_00baa7e8;
              fVar13 = local_58;
              FUN_0041d540();
              local_68 = fVar13 * local_5c;
              local_64 = local_5c * local_60;
              local_54 = (float)(*(int *)(iVar8 + 0x24) % *(int *)(DAT_00c71678[0x60c0] + 0xc)) *
                         DAT_00baa904 + DAT_00baa904;
              local_50 = (float)(*(int *)(iVar8 + 0x24) / *(int *)(DAT_00c71678[0x60c0] + 0xc)) *
                         DAT_00baa904 + DAT_00baaa00;
              piVar6 = (int *)FUN_00428b20(1000,99,&local_54,&local_68,0,1,uVar4);
              piVar6[0x106] = 0x3f800000;
              piVar6[0x39] = (int)((float)piVar6[0x39] + (float)piVar6[0x39]);
              piVar6[0x3a] = (int)((float)piVar6[0x3a] + (float)piVar6[0x3a]);
              iVar2 = FUN_006eef60();
              piVar6[0x5b] = piVar6[0x5b] | 0x1000;
              dVar14 = (double)(&DAT_00bacb00)[-(iVar2 >> 0x1f)];
              piVar6[0x5a] = piVar6[0x5a];
              piVar6[0x105] =
                   (int)(DAT_00baadb4 -
                        (float)((double)iVar2 + dVar14) * DAT_00ba9ff4 * DAT_00baa75c);
              (**(code **)(*piVar6 + 0xc))();
              local_38 = (int *)((int)local_38 + -1);
            } while (local_38 != (int *)0x0);
            local_38 = (int *)0x0;
            param_1 = local_4c;
            piVar7 = local_34;
          }
        }
      }
      cVar11 = local_2d;
      if ((*(int *)(local_44 + 0x74) != 0) && (*(char *)(local_44 + 0x84) != '\0')) {
        FUN_00409100();
        cVar11 = '\0';
      }
    }
    piVar6 = local_48;
    if (((piVar7 == (int *)0x0) || (local_48 == (int *)0x0)) || (local_40 < 6)) {
      if (cVar11 == '\0') goto LAB_0092f901;
    }
    else {
      FUN_00452bf0();
      local_8 = 0;
      FUN_007abe20();
      local_8 = 0xffffffff;
      if (0xf < local_18) {
        uVar10 = local_18 + 1;
        uVar3 = local_2c;
        if (0xfff < uVar10) {
          uVar3 = *(uint *)(local_2c - 4);
          uVar10 = local_18 + 0x24;
          if (0x1f < (local_2c - uVar3) - 4) {
                    /* WARNING: Subroutine does not return */
            _invalid_parameter_noinfo_noreturn();
          }
        }
        FUN_00aef15c(uVar3,uVar10);
      }
      iVar8 = piVar7[0x6c8];
      local_1c = 0;
      local_18 = 0xf;
      local_2c = local_2c & 0xffffff00;
      piVar6[0x6c7] = piVar7[0x6c7];
      piVar6[0x6c8] = iVar8;
LAB_0092f901:
      if (param_1[4] != 1) break;
    }
    piVar6 = (int *)DAT_00c71678[0x6eaa];
    if (piVar6 != (int *)DAT_00c71678[0x6eab]) {
      piVar7 = (int *)DAT_00c71678[0x6eab];
      do {
        iVar8 = *piVar6;
        if ((iVar8 != 0) && (*(int *)(iVar8 + 0x2c) == 0)) {
          *(float *)(iVar8 + 0xdc) = DAT_00c7b640;
          *(float *)(iVar8 + 0xe0) = DAT_00c7b644;
        }
        piVar6 = piVar6 + 1;
      } while (piVar6 != piVar7);
    }
    if ((0x14 < (uint)param_1[1]) || ((param_1[4] == 1 && (5 < (uint)param_1[1])))) {
      param_1[1] = 0;
      *param_1 = 2;
      FUN_007ea5d0();
      FUN_0092e300();
      if ((param_1[4] == 4) && (iVar8 = FUN_006f9d20(), iVar8 != 0)) {
        if (iVar8 == 0xff) {
          Isaac__log(1,"[warn] No ending for big chest!\n");
          FUN_00704f20();
          *param_1 = 4;
        }
        else {
          if ((char)DAT_00c71678[0x9655] == '\0') {
            FUN_006f9770();
          }
          *param_1 = 4;
        }
      }
    }
    break;
  case 2:
    uVar3 = param_1[1];
    uVar10 = param_1[2];
    if (uVar3 < uVar10) {
      if (uVar3 == uVar10 - 2) {
        if ((char)param_1[3] == '\0') {
          iVar8 = param_1[4];
          if (iVar8 == 2) {
            FUN_007466d0(0xb,0);
          }
          else if (iVar8 == 3) {
            FUN_007466d0(0xc,0);
          }
          else if (iVar8 == 6) {
            FUN_007466d0(0xd,0);
          }
          else {
            FUN_007467c0();
          }
        }
        else {
          cVar11 = FUN_00665c60();
          if (cVar11 != '\0') {
            cVar11 = Level__curse_mode_predicate();
            if (cVar11 == '\0') {
              iVar8 = (~DAT_00c71678[0x9a71] & 1U) + 1;
            }
            else {
              iVar8 = 1;
            }
            FUN_007466d0(iVar8);
            Seeds__advance_stage_slot();
          }
        }
        if (*(int *)(DAT_00c7169c + 0x4b3d8) != *(int *)(DAT_00c7169c + 0x4b3dc)) {
          FUN_0090df40();
        }
        break;
      }
      if ((uVar3 != uVar10 - 1) || ((char)param_1[5] != '\0')) break;
      cVar11 = FUN_0074f090();
      bVar12 = cVar11 == '\0';
LAB_0092fe68:
      if (!bVar12) break;
    }
    else {
      param_1[1] = 0;
      *param_1 = 3;
      if (uVar10 == 8) {
        param_1[2] = 0xf;
      }
      piVar6 = DAT_00c71678;
      if (param_1[4] == 1) {
        piVar6 = (int *)DAT_00c71678[0x6eaa];
        piVar7 = DAT_00c71678;
        if (piVar6 != (int *)DAT_00c71678[0x6eab]) {
          do {
            iVar8 = *piVar6;
            if ((iVar8 != 0) && (*(int *)(iVar8 + 0x2c) == 0)) {
              if (iVar8 == piVar7[0x6edc]) {
                FUN_007ab380(0x7f,"Pickup","PlayerPickupSparkle");
                piVar7 = DAT_00c71678;
              }
              else {
                FUN_007abe20();
                piVar7 = DAT_00c71678;
              }
            }
            piVar6 = piVar6 + 1;
          } while (piVar6 != (int *)piVar7[0x6eab]);
        }
      }
      else if (((param_1[4] != 5) && (cVar11 = FUN_0074f090(), cVar11 == '\0')) &&
              (piVar7 = (int *)piVar6[0x6eaa], piVar7 != (int *)piVar6[0x6eab])) {
        do {
          if ((*piVar7 != 0) && (*(int *)(*piVar7 + 0x2c) == 0)) {
            FUN_007abe20();
            piVar6 = DAT_00c71678;
          }
          piVar7 = piVar7 + 1;
        } while (piVar7 != (int *)piVar6[0x6eab]);
      }
      FUN_004186c0();
      piVar6 = (int *)DAT_00c71678[0x6eaa];
      piVar7 = DAT_00c71678;
      if (piVar6 != (int *)DAT_00c71678[0x6eab]) {
        do {
          piVar1 = (int *)*piVar6;
          if ((piVar1 != (int *)0x0) && (piVar1[0xb] == 0)) {
            (**(code **)(*piVar1 + 0xc))();
            piVar7 = DAT_00c71678;
            *(undefined1 *)((int)piVar1 + 0x171) = 1;
          }
          piVar6 = piVar6 + 1;
        } while (piVar6 != (int *)piVar7[0x6eab]);
      }
      if ((char)piVar7[4] == '\0') {
        piVar7[0x9958] = piVar7[0x9958] + 1;
        if (1 < piVar7[0x9958]) {
          FUN_00929a20();
          piVar7 = DAT_00c71678;
        }
      }
      else {
        piVar7[0x9958] = 0;
      }
      if ((*(byte *)(piVar7 + 0x60e7) & 0x20) == 0) {
        piVar7[0x9959] = piVar7[0x9959] + 1;
        if (1 < piVar7[0x9959]) {
          FUN_00929a20();
          piVar7 = DAT_00c71678;
        }
      }
      else {
        piVar7[0x9959] = 0;
      }
      if ((((piVar7[0x9a72] != 2) && (piVar7[0x9a72] != 3)) && (*piVar7 == 7)) &&
         ((piVar7[1] == 4 || (piVar7[1] == 5)))) {
        FUN_00929a20();
        piVar7 = DAT_00c71678;
      }
      if (param_1[4] == 5) {
        piVar7[0x9953] = piVar7[0x9953] | 0x10000;
        piVar7[0x9952] = piVar7[0x9952];
        if (param_1[4] != 5) goto LAB_0092fbfd;
LAB_0092fc1b:
        local_38 = (int *)0x267;
        FUN_00956780();
        FUN_0092dc30(local_38,0x3f800000,2,0,0x3f800000,0);
      }
      else {
LAB_0092fbfd:
        if (((0 < *piVar7) && (*piVar7 < 7)) && ((piVar7[0x9953] & 0x10000U) != 0))
        goto LAB_0092fc1b;
      }
      Level__Init();
      FUN_00802980();
      FUN_00958ed0();
      FUN_009bc000();
      piVar6 = DAT_00c71678;
      if ((DAT_00c71678[0x9961] == 0x1f) && (*DAT_00c71678 != 0xb)) {
        piVar7 = (int *)DAT_00c71678[0x6eaa];
        if (piVar7 != (int *)DAT_00c71678[0x6eab]) {
          do {
            iVar8 = *piVar7;
            if ((iVar8 != 0) && (*(int *)(iVar8 + 0x2c) == 0)) {
              *(undefined1 *)(iVar8 + 0x1398) = 0;
              *(undefined1 *)(iVar8 + 0x139a) = 0;
            }
            piVar7 = piVar7 + 1;
          } while (piVar7 != (int *)piVar6[0x6eab]);
        }
        FUN_0082ee40(DAT_00c71678[DAT_00c71678[0x60c5] * 0x2e + 5],0xffffffff,0xf,0,0xffffffff);
        FUN_008318a0();
        iVar8 = FUN_00740bc0(DAT_00c71678[0x60b4],0xffffffff);
        *(uint *)(iVar8 + 0x44) = *(uint *)(iVar8 + 0x44) & 0xfffffffe;
        FUN_0073f940();
        *param_1 = 0;
      }
      if ((char)param_1[5] == '\0') break;
      if ((0 < *DAT_00c71678) && (*DAT_00c71678 < 7)) {
        bVar12 = (DAT_00c71678[0x9953] & 0x10000U) == 0;
        goto LAB_0092fe68;
      }
    }
    iVar2 = DAT_00c7169c;
    iVar8 = param_1[3];
    *(undefined1 *)(DAT_00c7169c + 0x4b2a4) = 1;
    *(char *)(iVar2 + 0x4b2a5) = (char)iVar8;
    break;
  case 3:
    uVar3 = param_1[1];
    if ((uVar3 == 2) && ((char)param_1[5] != '\0')) {
      FUN_007eb1b0(local_14);
      uVar3 = param_1[1];
    }
    if ((uint)param_1[2] <= uVar3) {
      param_1[1] = 0;
      *param_1 = 4;
      FUN_00746560();
    }
    break;
  case 4:
    local_2e = '\x01';
    FUN_004186c0();
    piVar6 = (int *)DAT_00c71678[0x6eaa];
    piVar7 = DAT_00c71678;
    cVar11 = local_2e;
    if (piVar6 == (int *)DAT_00c71678[0x6eab]) {
LAB_0092ff4d:
      *param_1 = 0;
    }
    else {
      do {
        piVar1 = (int *)*piVar6;
        if ((piVar1 != (int *)0x0) && (piVar1[0xb] == 0)) {
          (**(code **)(*piVar1 + 0xc))();
          if (((char)piVar1[0x4e6] == '\0') && (*(char *)((int)piVar1 + 0x139a) == '\0')) {
            *(undefined1 *)(piVar1 + 0x104) = 1;
            piVar7 = DAT_00c71678;
          }
          else {
            cVar11 = '\0';
            piVar7 = DAT_00c71678;
          }
        }
        piVar6 = piVar6 + 1;
      } while (piVar6 != (int *)piVar7[0x6eab]);
      param_1 = local_4c;
      if (cVar11 != '\0') goto LAB_0092ff4d;
    }
    FUN_009aca90();
  }
  param_1[1] = param_1[1] + 1;
  piVar6 = DAT_00c71678;
  if ((*param_1 == 3) || (*param_1 == 2)) {
    DAT_00c71678[0x8bb5] = 2;
    piVar6[0x8bb7] = 2;
  }
  ExceptionList = local_10;
  return;
}
