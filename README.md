# NUC5G Power Consumption Testbed

Collection of scripts and configuration files used in our testbed to measure the power consumption of different 5G core network deployments. 
Gathered metrics can be found at [5GC power consumption data](https://github.com/IncludeArthur/5GC-power-consumption-data/tree/main).

## Testbed architecture
The testbed comprises 5 Intel NUC units, the 3 used for the 5GC deployments have the following specifications: 
- i5-7260U processor @2.20GHz
- 8GB of RAM
- 240GB SSD
- 1 Gigabit Ethernet and Dual Band Wireless connectivity
- Ubuntu 20.04 Desktop OS

<!-- end of the list -->

We also used the follwoing software:
- [Open5GS](https://open5gs.org/)
- [Free5GC](https://free5gc.org/)
- [UERANSIM](https://github.com/aligungr/UERANSIM)
- [Redis](https://redis.io/)
- [Scaphandre](https://github.com/hubblo-org/scaphandre)
- Iperf3

<!-- end of the list -->

The power consumption data is gathered using both hardware-based (Meross MSS310 smart-plugs) and software-based (Scaphandre) power meters.

<p align="center">
  <img width="600" src="https://github.com/IncludeArthur/power-consumption-data/assets/44785274/6fa210b5-d047-44c0-8432-f27085b44e5c">
</p>

## Publications
Please cite our published papers if you intend on using the data or code in this repository

> * A. Bellin, M. Centenaro and F. Granelli, "A Preliminary Study on the Power Consumption of Virtualized Edge 5G Core Networks," 2023 IEEE 9th International Conference on Network Softwarization (NetSoft), Madrid, Spain, 2023, pp. 420-425, doi: 10.1109/NetSoft57336.2023.10175489.
> * A. Bellin, F. Granelli, and D. Munaretto, "A measurement-based approach to analyze the power consumption of the softwarized 5G core," Computer Networks, vol. 244, p. 110 312, 2024, doi: 10.1016/j.comnet.2024.110312.
