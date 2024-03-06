# O3R docker manager

## Why this library exists

The o3r camera system is setup to facilitate the usage of docker containers to deploy applications to the VPU (OVPxxx).

The ifm3d c++/python api allows a developer to write applications using the o3r on their local machine and then recompile those applications to run directly on the VPU with minimal overhead. This library incorporates lesson from the ifm3d.com documentation on docker implementations. For each robust production ready solution a few common tools and practices are standard. An opinionated set of these tools are provided by this o3r deployment library to facilitate convenient and reliable deployment of 3rd party applications to the o3r platform.

- System for setting up and sharing a common directory between the running application and the rest of the VPU (see docker volumes documentation)
- Reccommended log cache file structure and logging tools for python (and soon c++)
- System for collating application logs in a consistent way whenever the developer connects to the vpu to perform updates/troubleshooting
- "One-click" solution deployment scripting

The following architecture is prescribed to minimize feedback loops during the development process:

![](schematic.drawio.svg)


## Quick start (from source)

`pip install -e ./ovp_docker_manager`

Check out the [deployment example](./deployment_example/README.md) for all of the components needed for a basic deployment of an application
