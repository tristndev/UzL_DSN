# Tutorial 4

## Ex 01: Distance from RSSI

1. TODO: Find out address of target pi (1m distance) and set in line 36.
2. Press `LEFT` to init rssi calculation (ignore the distance calculation).
3. Set measured RSSI as reference `A` in line 48.
4. Press `LEFT` to init new rssi_calculation (now consider the distance calculation).

## Ex 02: Localization with three anchors

### Bounding Box 

0. Set PAN.
1. Initiate ping broadcast, direction `DOWN`.
2. Once pongs came back, calc bbox localization with direction `RIGHT`.

### Multilateration

0. Run `pip install localization` for the needed package.
1. Initiate ping broadcast, direction `DOWN`.
2. Once pongs came back, calc multilateration localization with direction `UP`.