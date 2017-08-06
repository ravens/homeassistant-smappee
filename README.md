# homeassistant-smappee
A custom component to retrieve Power and Cos Phi value of a local Smappee power meter. 

![Screenshot of smappee states](screenshot-hass-smappee.png)

## Description

This is a minimalistic custom components for home-assistant. It uses the local API of the embedded web server of the smappee power meter. 

## Configuration

Once the custom_components smappee python file have been copied in your configuration directory, add a smappee component with a host parameter to reacht the smappee. By default the data is retrieved every 30s. 

## API playground

A Jupyter [Notebook](api-smappee.ipynb) can be used to toy with the API on the smappee. At the moment we only play with the instantaneous values. 

## Demo environment

A docker-compose YAML [file](docker-compose.yml) is provided to run the component. 
