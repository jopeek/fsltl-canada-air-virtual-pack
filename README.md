# fsltl-canada-air-virtual-pack
An add-on library of FSLTL compatible Canada Air Virtual liveries.

Requires the FSLTL Base Models available from https://fslivetrafficliveries.com/

## How to Install
- **Easiest:** in CAVacars 2, open Settings and install the pack from there. CAVacars also tells you when an update is out.
- **By hand:** download `fsltl-canada-air-virtual-pack.zip` from the [latest release](https://github.com/jopeek/fsltl-canada-air-virtual-pack/releases/latest) (not the "Source code" zip) and unzip it into your sim's Community folder, so you get a folder named exactly `fsltl-canada-air-virtual-pack`. Delete any older copy first, such as `fsltl-canada-air-virtual-pack-1.0`.
- (optional for UniFly) Copy the `FSLTLCAV.vmr` file into the `%localappdata%/UniFly/rulesets` folder and restart UniFly if it's currently running


## Releasing
1. Bump `package_version` in `manifest.json` and run `build.bat` (or `python3 build.py`) to refresh `layout.json` and the VMR.
2. Commit, then push a tag that matches the version: `git tag v1.2.0 && git push origin v1.2.0`.
3. The Release workflow builds the zip and publishes the release with the zip and `manifest.json` attached. CAVacars 2 picks it up from there.
