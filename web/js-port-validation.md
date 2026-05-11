# JavaScript Port Validation

## Checks

1. Open `web/index.html` in a browser and confirm the canvas renders.
2. Verify that the simulation starts automatically without console errors.
3. Confirm the frame info label updates with a delta time value.
4. Confirm that same-size squares do not trigger eating.
5. Confirm that larger nearby squares push smaller squares away and that larger squares chase smaller ones.
6. Run `window.runSpeedTest()` in the browser console and confirm it returns `true`.

## Notes

- The browser version should preserve the Python update order, not redesign the behavior.
- The expected output is a working standalone HTML simulation, not a framework app.