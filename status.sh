#!/bin/bash
dbus-send --session --print-reply --dest=gyro.monitor.TriggerService /gyro/monitor/TriggerService gyro.monitor.TriggerInterface.status