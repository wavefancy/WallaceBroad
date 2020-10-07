## Optimized terra jupter Docker image 

## Version 1.6
- `sudo apt-get install datamash`

### Check out the latest version [here](https://hub.docker.com/r/wavefancy/terrawngs/tags), in Terra make a custom ENV by `<image_name>:<tag>`
- The latest version: `wavefancy/terrawngs:v1.5`
- Terra will not remove your files if change VM config but not the disk size.

### Updates in the base image
- Based on the [Terra base images](https://github.com/DataBiosphere/terra-docker), April 20, 2020.
- Upgrade to have root permission (atbroad)
- Keep the update list for apt-get, 
  keep the ability to install software by apt-get
  
- Installed tools: less htop sysstat(iostat) psmisc(killall) tabix
- Fix the file ownership in the home folder.

### Derived ngs tools Docker image
- Ported own python scripts and R scripts tools
- Update bash config files
  - fix time Zone: `export TZ=America/New_York`
  - installed tmux, and tmux session save plugin [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect).
  - installed vim and plugins, fixed various problem.
  - fix vim color issue in tmux: `export TERM=xterm-256color`
    [Ref here](https://vi.stackexchange.com/questions/10708/no-syntax-highlighting-in-tmux)
    
- Installed Jupyter [bash kernel](https://github.com/takluyver/bash_kernel).
- Installed Jupyter R kernel.
- Add/Change/Check Jupyter kernel config: `jupyter kernelspec list`
- Add `body` function to bash config, [more details](https://unix.stackexchange.com/questions/11856/sort-but-keep-header-line-at-the-top).  
