// https://github.com/khanning/littlebits-ble-extension/blob/gh-pages/littleBitsBLE_extension.js

/*This program is free software: you can redistribute it and/or modify
 *it under the terms of the GNU General Public License as published by
 *the Free Software Foundation, either version 3 of the License, or
 *(at your option) any later version.
 *
 *This program is distributed in the hope that it will be useful,
 *but WITHOUT ANY WARRANTY; without even the implied warranty of
 *MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *GNU General Public License for more details.
 *
 *You should have received a copy of the GNU General Public License
 *along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

(function(ext) {

  var UUID = '0705d0c0c8d841c9ae1552fad5358b8a',
    TX_CHAR = '0705d0c2c8d841c9ae1552fad5358b8a';
    RX_CHAR = '0705d0c2c8d841c9ae1552fad5358b8a';

  var device = null;

  var rx = {};
  rx[RX_CHAR] = {notify: true};
  var tx = {};
  tx[TX_CHAR] = {};

  var device_info = {uuid: [UUID]};
  device_info["read_characteristics"] = rx;
  device_info["write_characteristics"] = tx;

  var inputVal = 0;

  function map(val, aMin, aMax, bMin, bMax) {
    if (val > aMax) val = aMax;
    else if (val < aMin) val = aMin;
    return (((bMax - bMin) * (val - aMin)) / (aMax - aMin)) + bMin;
  }

  ext.whenInput = function(state) {
    if (state === 'on') return inputVal > 1;
    else if (state === 'off') return inputVal === 0;
    return false;
  };

  ext.whenInputCompare = function(op, val) {
    val = parseInt(val);
    if (isNaN(val)) return false;
    if (op === '>') return inputVal > val;
    else if (op === '<') return inputVal < val;
    else if (op === '=') return inputVal === val;
    return false;
  };

  ext.getInput = function() {
    return inputVal;
  };

  ext.turnOutput = function(val) {
    if (val === 'on') val = 100;
    else if (val === 'off') val = 0;
    var output = [0, 2, Math.round(map(val, 0, 100, 0, 255))];
    device.emit('write', {uuid: TX_CHAR, bytes: output});
  };

  ext.sendOutput = function(val) {
    if (val > 100) val = 100;
    else if (val < 0) val = 0;
    var output = [0, 2, Math.round(map(val, 0, 100, 0, 255))];
    device.emit('write', {uuid: TX_CHAR, bytes: output});
  };

  ext._getStatus = function() {
    if (device) {
      if (device.is_open()) {
        return {status: 2, msg: 'littleBits connected'};
      } else {
        return {status: 1, msg: 'littleBits connecting...'};
      }
    } else {
      return {status: 1, msg: 'littleBits disconnected'};
    }
  };

  ext._deviceConnected = function(dev) {
    if (device) return;
    device = dev;
    device.open(function(d) {
      if (device == d) {
        device.on(RX_CHAR, function(bytes) {
          if (bytes.data.length === 4)
            inputVal = Math.round(map(bytes.data[2], 0, 255, 0, 100));
          else return;
        });
      } else if (d) {
        console.log('Received open callback for wrong device');
      } else {
        console.log('Opening device failed');
        device = null;
      }
    });
  };

  ext._deviceRemoved = function(dev) {
    rawData = [];
    if (device != dev) return;
    device = null;
  };

  ext._shutdown = function() {
    if (device) device.close();
    device = null;
  };

  var blocks = [
    ['h', 'when input is %m.dStates', 'whenInput', 'on'],
    ['h', 'when input is %m.ops %n', 'whenInputCompare', '>', 50],
    ['r', 'input', 'getInput'],
    [' '],
    [' ', 'turn output %m.dStates', 'turnOutput', 'on'],
    [' ', 'set output to %n%', 'sendOutput', 100]
  ];

  var menus = {
    dStates: ['on', 'off'],
    ops: ['>', '<', '=']
  };

  var descriptor = {
    blocks: blocks,
    menus: menus,
    url: 'http://scratch.mit.edu'
  };

  ScratchExtensions.register('littleBits BLE w30', descriptor, ext, {info: device_info, type: 'ble'});
})({});
