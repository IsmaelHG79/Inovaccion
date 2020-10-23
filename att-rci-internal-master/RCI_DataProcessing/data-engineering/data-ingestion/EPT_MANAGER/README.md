<a name="main"></a>  ![Encabezado](./images/encabezado.png)

----

# Documentación Data Ingestion para la fuente ATT **EPT MANAGER**

El procesamiento de carga de esta fuente se realiza a partir de archivos excel los cuales contienen diferentes sheets (Hojas de cálculo), en donde cada sheet se cargara a su respectiva tabla. Les hojas de cálculo seleccionadas son y son las siguientes:

1. **EPT_3G_LTE_OUTDOOR**
2. **EPT_3G_LTE_INDOOR**
3. **PLAN_OUTDOOR**
4. **PLAN_INDOOR**
5. **Eventos_Especiales**


## Descripcion del *`FTP`*

El diseño del Data Lake se detalla en el documento [Diseño del DataLake](http://10.103.133.122/app/owncloud/f/14480776), en este se especifican:

- El servidor y la ruta en donde se encontrarán los archivos a ingestar.

- La ruta en donde se coloca el respaldo de los archivos ingestados.

- El directorio de HDFS en donde se colocan los datos ingestados.

## Descripcion de la fuentes de datos

- **[descripcion]** Descripcion basada en la documentacion del EDA para esta fuente se encuentra descrita aqui **[Descripcion EDA EPT_Manager](/RCI_DataAnalysis/eda/EPT_Manager/README.md#descripcion)**

- **[dicciorario de datos]** La siguiente tabla muestra el resultado de ejecutar el siguiente comando: 
    
```
describe formatted rci_network_db.tx_ept_lte_outdoor;
```
    
| col_name | data_type | comment |
|--------------------|-----------|------------------------------------------|
| att_site_name | string | Type inferred from 'kite' |
| att_node_name | string | Type inferred from 'kite' |
| att_name | string | Type inferred from 'kite' |
| att_tech | string | Type inferred from 'kite' |
| att_cell_id | string | Type inferred from 'kite' |
| att_cell_id_name | string | Type inferred from 'kite' |
| node_b_u2000 | string | Type inferred from 'kite' |
| name | string | Type inferred from 'kite' |
| latitud | string | Type inferred from 'kite' |
| longitud | string | Type inferred from 'kite' |
| state | string | Type inferred from 'kite' |
| id_state | string | Type inferred from 'kite' |
| country | string | Type inferred from 'kite' |
| id_country | string | Type inferred from 'kite' |
| region | string | Type inferred from 'kite' |
| market | string | Type inferred from 'kite' |
| distance_from_mex_usa_border_line_miles | string | Type inferred from 'kite' |
| range | string | Type inferred from 'kite' |
| time_zone | string | Type inferred from 'kite' |
| cell_average_heihgt | string | Type inferred from 'kite' |
| altitude_m | string | Type inferred from 'kite' |
| solution | string | Type inferred from 'kite' |
| coverage | string | Type inferred from 'kite' |
| infraestructure_type | string | Type inferred from 'kite' |
| owner | string | Type inferred from 'kite' |
| mcc | string | Type inferred from 'kite' |
| mnc | string | Type inferred from 'kite' |
| nir | string | Type inferred from 'kite' |
| propagation_model | string | Type inferred from 'kite' |
| cell_radius_m | string | Type inferred from 'kite' |
| traffic_of_last_month | string | Type inferred from 'kite' |
| frec | string | Type inferred from 'kite' |
| band_indicator | string | Type inferred from 'kite' |
| band | string | Type inferred from 'kite' |
| band_width | string | Type inferred from 'kite' |
| ul_fc_mhz | string | Type inferred from 'kite' |
| dl_fc_mhz | string | Type inferred from 'kite' |
| ul_uarfcn_earfcn | string | Type inferred from 'kite' |
| dl_uarfcn_earfcn | string | Type inferred from 'kite' |
| carrier | string | Type inferred from 'kite' |
| cellname | string | Type inferred from 'kite' |
| node_b_id | string | Type inferred from 'kite' |
| physical_sector | string | Type inferred from 'kite' |
| cell_id | string | Type inferred from 'kite' |
| local_cell_id | string | Type inferred from 'kite' |
| psc_pci | string | Type inferred from 'kite' |
| rnc | string | Type inferred from 'kite' |
| rnc_id | string | Type inferred from 'kite' |
| lac_tal | string | Type inferred from 'kite' |
| tac | string | Type inferred from 'kite' |
| rac | string | Type inferred from 'kite' |
| ura | string | Type inferred from 'kite' |
| sac | string | Type inferred from 'kite' |
| time_offset | string | Type inferred from 'kite' |
| max_transmit_power_of_cell | string | Type inferred from 'kite' |
| pcpich_rs_power | string | Type inferred from 'kite' |
| antenna_height | string | Type inferred from 'kite' |
| geographic_azimuth | string | Type inferred from 'kite' |
| magnetic_declination | string | Type inferred from 'kite' |
| magnetic_azimuth | string | Type inferred from 'kite' |
| mech_tilt | string | Type inferred from 'kite' |
| elect_tilt | string | Type inferred from 'kite' |
| antenna_count_per_sector | string | Type inferred from 'kite' |
| antenna_model | string | Type inferred from 'kite' |
| beam_width | string | Type inferred from 'kite' |
| root_sequence_idx | string | Type inferred from 'kite' |
| tx_rx | string | Type inferred from 'kite' |
| ept_date | string | Type inferred from 'kite' |
| project | string | Type inferred from 'kite' |
| batch | string | Type inferred from 'kite' |
| update_type | string | Type inferred from 'kite' |
| update_date | string | Type inferred from 'kite' |
| vendor | string | Type inferred from 'kite' |
| cluster | string | Type inferred from 'kite' |
| operador | string | Type inferred from 'kite' |
| tracker | string | Type inferred from 'kite' |
| asl_local | string | Type inferred from 'kite' |
| asl_ift | string | Type inferred from 'kite' |
| nir_ift | string | Type inferred from 'kite' |
| prefix_911 | string | Type inferred from 'kite' |
| prefix_89 | string | Type inferred from 'kite' |
| region_celular | string | Type inferred from 'kite' |
| region_pcs | string | Type inferred from 'kite' |
| municipio | string | Type inferred from 'kite' |
| id_location_sir | string | Type inferred from 'kite' |
| location_sir | string | Type inferred from 'kite' |
| comentario | string | Type inferred from 'kite' |
| cs_pool | string | Type inferred from 'kite' |
| id_country_sir | string | Type inferred from 'kite' |
| country_sir | string | Type inferred from 'kite' |
| ps_pool | string | Type inferred from 'kite' |
| ne_name | string | Type inferred from 'kite' |
| enodeb_function | string | Type inferred from 'kite' |
| index | string | Type inferred from 'kite' |
| node_b_u2000_anterior | string | Type inferred from 'kite' |
| cellname_anterior | string | Type inferred from 'kite' |

```
describe formatted rci_network_db.tx_ept_lte_indoor;
```
    
| col_name | data_type | comment |
|--------------------|-----------|------------------------------------------|
| att_site_name | string | Type inferred from 'kite' |
| att_node_name | string | Type inferred from 'kite' |
| att_name | string | Type inferred from 'kite' |
| att_tech | string | Type inferred from 'kite' |
| att_cell_id | string | Type inferred from 'kite' |
| att_cell_id_name | string | Type inferred from 'kite' |
| node_b_u2000 | string | Type inferred from 'kite' |
| name | string | Type inferred from 'kite' |
| latitud | string | Type inferred from 'kite' |
| longitud | string | Type inferred from 'kite' |
| state | string | Type inferred from 'kite' |
| id_state | string | Type inferred from 'kite' |
| country | string | Type inferred from 'kite' |
| id_country | string | Type inferred from 'kite' |
| region | string | Type inferred from 'kite' |
| market | string | Type inferred from 'kite' |
| distance_from_mex_usa_border_line_miles | string | Type inferred from 'kite' |
| range | string | Type inferred from 'kite' |
| time_zone | string | Type inferred from 'kite' |
| cell_average_heihgt | string | Type inferred from 'kite' |
| altitude_m | string | Type inferred from 'kite' |
| solution | string | Type inferred from 'kite' |
| coverage | string | Type inferred from 'kite' |
| infraestructure_type | string | Type inferred from 'kite' |
| owner | string | Type inferred from 'kite' |
| mcc | string | Type inferred from 'kite' |
| mnc | string | Type inferred from 'kite' |
| nir | string | Type inferred from 'kite' |
| propagation_model | string | Type inferred from 'kite' |
| cell_radius_m | string | Type inferred from 'kite' |
| traffic_of_last_month | string | Type inferred from 'kite' |
| frec | string | Type inferred from 'kite' |
| band_indicator | string | Type inferred from 'kite' |
| band | string | Type inferred from 'kite' |
| band_width | string | Type inferred from 'kite' |
| ul_fc_mhz | string | Type inferred from 'kite' |
| dl_fc_mhz | string | Type inferred from 'kite' |
| ul_uarfcn_earfcn | string | Type inferred from 'kite' |
| dl_uarfcn_earfcn | string | Type inferred from 'kite' |
| carrier | string | Type inferred from 'kite' |
| cellname | string | Type inferred from 'kite' |
| node_b_id | string | Type inferred from 'kite' |
| physical_sector | string | Type inferred from 'kite' |
| cell_id | string | Type inferred from 'kite' |
| local_cell_id | string | Type inferred from 'kite' |
| psc_pci | string | Type inferred from 'kite' |
| rnc | string | Type inferred from 'kite' |
| rnc_id | string | Type inferred from 'kite' |
| lac_tal | string | Type inferred from 'kite' |
| tac | string | Type inferred from 'kite' |
| rac | string | Type inferred from 'kite' |
| ura | string | Type inferred from 'kite' |
| sac | string | Type inferred from 'kite' |
| time_offset | string | Type inferred from 'kite' |
| max_transmit_power_of_cell | string | Type inferred from 'kite' |
| pcpich_rs_power | string | Type inferred from 'kite' |
| antenna_height | string | Type inferred from 'kite' |
| geographic_azimuth | string | Type inferred from 'kite' |
| magnetic_declination | string | Type inferred from 'kite' |
| magnetic_azimuth | string | Type inferred from 'kite' |
| mech_tilt | string | Type inferred from 'kite' |
| elect_tilt | string | Type inferred from 'kite' |
| antenna_count_per_sector | string | Type inferred from 'kite' |
| antenna_model | string | Type inferred from 'kite' |
| beam_width | string | Type inferred from 'kite' |
| root_sequence_idx | string | Type inferred from 'kite' |
| tx_rx | string | Type inferred from 'kite' |
| ept_date | string | Type inferred from 'kite' |
| project | string | Type inferred from 'kite' |
| batch | string | Type inferred from 'kite' |
| update_type | string | Type inferred from 'kite' |
| update_date | string | Type inferred from 'kite' |
| vendor | string | Type inferred from 'kite' |
| cluster | string | Type inferred from 'kite' |
| operador | string | Type inferred from 'kite' |
| tracker | string | Type inferred from 'kite' |
| asl_local | string | Type inferred from 'kite' |
| asl_ift | string | Type inferred from 'kite' |
| nir_ift | string | Type inferred from 'kite' |
| prefix_911 | string | Type inferred from 'kite' |
| prefix_89 | string | Type inferred from 'kite' |
| region_celular | string | Type inferred from 'kite' |
| region_pcs | string | Type inferred from 'kite' |
| municipio | string | Type inferred from 'kite' |
| id_location_sir | string | Type inferred from 'kite' |
| location_sir | string | Type inferred from 'kite' |
| comentario | string | Type inferred from 'kite' |
| cs_pool | string | Type inferred from 'kite' |
| id_country_sir | string | Type inferred from 'kite' |
| country_sir | string | Type inferred from 'kite' |
| ps_pool | string | Type inferred from 'kite' |
| ne_name | string | Type inferred from 'kite' |
| enodeb_function | string | Type inferred from 'kite' |
| index | string | Type inferred from 'kite' |
| node_b_u2000_anterior | string | Type inferred from 'kite' |
| cellname_anterior | string | Type inferred from 'kite' |

```
describe formatted rci_network_db.tx_ept_plan_outdoor;
```
    
| col_name | data_type | comment |
|--------------------|-----------|------------------------------------------|
| att_site_name | string | Type inferred from 'kite' |
| att_node_name | string | Type inferred from 'kite' |
| att_name | string | Type inferred from 'kite' |
| att_tech | string | Type inferred from 'kite' |
| att_cell_id | string | Type inferred from 'kite' |
| att_cell_id_name | string | Type inferred from 'kite' |
| node_b_u2000 | string | Type inferred from 'kite' |
| name | string | Type inferred from 'kite' |
| latitud | string | Type inferred from 'kite' |
| longitud | string | Type inferred from 'kite' |
| state | string | Type inferred from 'kite' |
| id_state | string | Type inferred from 'kite' |
| country | string | Type inferred from 'kite' |
| id_country | string | Type inferred from 'kite' |
| region | string | Type inferred from 'kite' |
| market | string | Type inferred from 'kite' |
| distance_from_mex_usa_border_line_miles | string | Type inferred from 'kite' |
| range | string | Type inferred from 'kite' |
| time_zone | string | Type inferred from 'kite' |
| cell_average_heihgt | string | Type inferred from 'kite' |
| altitude_m | string | Type inferred from 'kite' |
| solution | string | Type inferred from 'kite' |
| coverage | string | Type inferred from 'kite' |
| infraestructure_type | string | Type inferred from 'kite' |
| owner | string | Type inferred from 'kite' |
| mcc | string | Type inferred from 'kite' |
| mnc | string | Type inferred from 'kite' |
| nir | string | Type inferred from 'kite' |
| propagation_model | string | Type inferred from 'kite' |
| cell_radius_m | string | Type inferred from 'kite' |
| traffic_of_last_month | string | Type inferred from 'kite' |
| frec | string | Type inferred from 'kite' |
| band_indicator | string | Type inferred from 'kite' |
| band | string | Type inferred from 'kite' |
| band_width | string | Type inferred from 'kite' |
| ul_fc_mhz | string | Type inferred from 'kite' |
| dl_fc_mhz | string | Type inferred from 'kite' |
| ul_uarfcn_earfcn | string | Type inferred from 'kite' |
| dl_uarfcn_earfcn | string | Type inferred from 'kite' |
| carrier | string | Type inferred from 'kite' |
| cellname | string | Type inferred from 'kite' |
| node_b_id | string | Type inferred from 'kite' |
| physical_sector | string | Type inferred from 'kite' |
| cell_id | string | Type inferred from 'kite' |
| local_cell_id | string | Type inferred from 'kite' |
| psc_pci | string | Type inferred from 'kite' |
| rnc | string | Type inferred from 'kite' |
| rnc_id | string | Type inferred from 'kite' |
| lac_tal | string | Type inferred from 'kite' |
| tac | string | Type inferred from 'kite' |
| rac | string | Type inferred from 'kite' |
| ura | string | Type inferred from 'kite' |
| sac | string | Type inferred from 'kite' |
| time_offset | string | Type inferred from 'kite' |
| max_transmit_power_of_cell | string | Type inferred from 'kite' |
| pcpich_rs_power | string | Type inferred from 'kite' |
| antenna_height | string | Type inferred from 'kite' |
| geographic_azimuth | string | Type inferred from 'kite' |
| magnetic_declination | string | Type inferred from 'kite' |
| magnetic_azimuth | string | Type inferred from 'kite' |
| mech_tilt | string | Type inferred from 'kite' |
| elect_tilt | string | Type inferred from 'kite' |
| antenna_count_per_sector | string | Type inferred from 'kite' |
| antenna_model | string | Type inferred from 'kite' |
| beam_width | string | Type inferred from 'kite' |
| root_sequence_idx | string | Type inferred from 'kite' |
| tx_rx | string | Type inferred from 'kite' |
| ept_date | string | Type inferred from 'kite' |
| project | string | Type inferred from 'kite' |
| batch | string | Type inferred from 'kite' |
| update_type | string | Type inferred from 'kite' |
| update_date | string | Type inferred from 'kite' |
| vendor | string | Type inferred from 'kite' |
| cluster | string | Type inferred from 'kite' |
| operador | string | Type inferred from 'kite' |
| tracker | string | Type inferred from 'kite' |
| asl_local | string | Type inferred from 'kite' |
| asl_ift | string | Type inferred from 'kite' |
| nir_ift | string | Type inferred from 'kite' |
| prefix_911 | string | Type inferred from 'kite' |
| prefix_89 | string | Type inferred from 'kite' |
| region_celular | string | Type inferred from 'kite' |
| region_pcs | string | Type inferred from 'kite' |
| municipio | string | Type inferred from 'kite' |
| id_location_sir | string | Type inferred from 'kite' |
| location_sir | string | Type inferred from 'kite' |
| comentario | string | Type inferred from 'kite' |
| cs_pool | string | Type inferred from 'kite' |
| id_country_sir | string | Type inferred from 'kite' |
| country_sir | string | Type inferred from 'kite' |
| ps_pool | string | Type inferred from 'kite' |
| ne_name | string | Type inferred from 'kite' |
| enodeb_function | string | Type inferred from 'kite' |
| index | string | Type inferred from 'kite' |
| node_b_u2000_anterior | string | Type inferred from 'kite' |
| cellname_anterior | string | Type inferred from 'kite' |


```
describe formatted rci_network_db.tx_ept_plan_indoor;
```
    
| col_name | data_type | comment |
|--------------------|-----------|------------------------------------------|
| att_site_name | string | Type inferred from 'kite' |
| att_node_name | string | Type inferred from 'kite' |
| att_name | string | Type inferred from 'kite' |
| att_tech | string | Type inferred from 'kite' |
| att_cell_id | string | Type inferred from 'kite' |
| att_cell_id_name | string | Type inferred from 'kite' |
| node_b_u2000 | string | Type inferred from 'kite' |
| name | string | Type inferred from 'kite' |
| latitud | string | Type inferred from 'kite' |
| longitud | string | Type inferred from 'kite' |
| state | string | Type inferred from 'kite' |
| id_state | string | Type inferred from 'kite' |
| country | string | Type inferred from 'kite' |
| id_country | string | Type inferred from 'kite' |
| region | string | Type inferred from 'kite' |
| market | string | Type inferred from 'kite' |
| distance_from_mex_usa_border_line_miles | string | Type inferred from 'kite' |
| range | string | Type inferred from 'kite' |
| time_zone | string | Type inferred from 'kite' |
| cell_average_heihgt | string | Type inferred from 'kite' |
| altitude_m | string | Type inferred from 'kite' |
| solution | string | Type inferred from 'kite' |
| coverage | string | Type inferred from 'kite' |
| infraestructure_type | string | Type inferred from 'kite' |
| owner | string | Type inferred from 'kite' |
| mcc | string | Type inferred from 'kite' |
| mnc | string | Type inferred from 'kite' |
| nir | string | Type inferred from 'kite' |
| propagation_model | string | Type inferred from 'kite' |
| cell_radius_m | string | Type inferred from 'kite' |
| traffic_of_last_month | string | Type inferred from 'kite' |
| frec | string | Type inferred from 'kite' |
| band_indicator | string | Type inferred from 'kite' |
| band | string | Type inferred from 'kite' |
| band_width | string | Type inferred from 'kite' |
| ul_fc_mhz | string | Type inferred from 'kite' |
| dl_fc_mhz | string | Type inferred from 'kite' |
| ul_uarfcn_earfcn | string | Type inferred from 'kite' |
| dl_uarfcn_earfcn | string | Type inferred from 'kite' |
| carrier | string | Type inferred from 'kite' |
| cellname | string | Type inferred from 'kite' |
| node_b_id | string | Type inferred from 'kite' |
| physical_sector | string | Type inferred from 'kite' |
| cell_id | string | Type inferred from 'kite' |
| local_cell_id | string | Type inferred from 'kite' |
| psc_pci | string | Type inferred from 'kite' |
| rnc | string | Type inferred from 'kite' |
| rnc_id | string | Type inferred from 'kite' |
| lac_tal | string | Type inferred from 'kite' |
| tac | string | Type inferred from 'kite' |
| rac | string | Type inferred from 'kite' |
| ura | string | Type inferred from 'kite' |
| sac | string | Type inferred from 'kite' |
| time_offset | string | Type inferred from 'kite' |
| max_transmit_power_of_cell | string | Type inferred from 'kite' |
| pcpich_rs_power | string | Type inferred from 'kite' |
| antenna_height | string | Type inferred from 'kite' |
| geographic_azimuth | string | Type inferred from 'kite' |
| magnetic_declination | string | Type inferred from 'kite' |
| magnetic_azimuth | string | Type inferred from 'kite' |
| mech_tilt | string | Type inferred from 'kite' |
| elect_tilt | string | Type inferred from 'kite' |
| antenna_count_per_sector | string | Type inferred from 'kite' |
| antenna_model | string | Type inferred from 'kite' |
| beam_width | string | Type inferred from 'kite' |
| root_sequence_idx | string | Type inferred from 'kite' |
| tx_rx | string | Type inferred from 'kite' |
| ept_date | string | Type inferred from 'kite' |
| project | string | Type inferred from 'kite' |
| batch | string | Type inferred from 'kite' |
| update_type | string | Type inferred from 'kite' |
| update_date | string | Type inferred from 'kite' |
| vendor | string | Type inferred from 'kite' |
| cluster | string | Type inferred from 'kite' |
| operador | string | Type inferred from 'kite' |
| tracker | string | Type inferred from 'kite' |
| asl_local | string | Type inferred from 'kite' |
| asl_ift | string | Type inferred from 'kite' |
| nir_ift | string | Type inferred from 'kite' |
| prefix_911 | string | Type inferred from 'kite' |
| prefix_89 | string | Type inferred from 'kite' |
| region_celular | string | Type inferred from 'kite' |
| region_pcs | string | Type inferred from 'kite' |
| municipio | string | Type inferred from 'kite' |
| id_location_sir | string | Type inferred from 'kite' |
| location_sir | string | Type inferred from 'kite' |
| comentario | string | Type inferred from 'kite' |
| cs_pool | string | Type inferred from 'kite' |
| id_country_sir | string | Type inferred from 'kite' |
| country_sir | string | Type inferred from 'kite' |
| ps_pool | string | Type inferred from 'kite' |
| ne_name | string | Type inferred from 'kite' |
| enodeb_function | string | Type inferred from 'kite' |
| index | string | Type inferred from 'kite' |
| node_b_u2000_anterior | string | Type inferred from 'kite' |
| cellname_anterior | string | Type inferred from 'kite' |


```
describe formatted rci_network_db.tx_ept_events_specials;
```
    
| col_name | data_type | comment |
|--------------------|-----------|------------------------------------------|
| att_site_name | string | Type inferred from 'kite' |
| att_node_name | string | Type inferred from 'kite' |
| att_name | string | Type inferred from 'kite' |
| att_tech | string | Type inferred from 'kite' |
| att_cell_id | string | Type inferred from 'kite' |
| att_cell_id_name | string | Type inferred from 'kite' |
| node_b_u2000 | string | Type inferred from 'kite' |
| name | string | Type inferred from 'kite' |
| latitud | string | Type inferred from 'kite' |
| longitud | string | Type inferred from 'kite' |
| state | string | Type inferred from 'kite' |
| id_state | string | Type inferred from 'kite' |
| country | string | Type inferred from 'kite' |
| id_country | string | Type inferred from 'kite' |
| region | string | Type inferred from 'kite' |
| market | string | Type inferred from 'kite' |
| distance_from_mex_usa_border_line_miles | string | Type inferred from 'kite' |
| range | string | Type inferred from 'kite' |
| time_zone | string | Type inferred from 'kite' |
| cell_average_heihgt | string | Type inferred from 'kite' |
| altitude_m | string | Type inferred from 'kite' |
| solution | string | Type inferred from 'kite' |
| coverage | string | Type inferred from 'kite' |
| infraestructure_type | string | Type inferred from 'kite' |
| owner | string | Type inferred from 'kite' |
| mcc | string | Type inferred from 'kite' |
| mnc | string | Type inferred from 'kite' |
| nir | string | Type inferred from 'kite' |
| propagation_model | string | Type inferred from 'kite' |
| cell_radius_m | string | Type inferred from 'kite' |
| traffic_of_last_month | string | Type inferred from 'kite' |
| frec | string | Type inferred from 'kite' |
| band_indicator | string | Type inferred from 'kite' |
| band | string | Type inferred from 'kite' |
| band_width | string | Type inferred from 'kite' |
| ul_fc_mhz | string | Type inferred from 'kite' |
| dl_fc_mhz | string | Type inferred from 'kite' |
| ul_uarfcn_earfcn | string | Type inferred from 'kite' |
| dl_uarfcn_earfcn | string | Type inferred from 'kite' |
| carrier | string | Type inferred from 'kite' |
| cellname | string | Type inferred from 'kite' |
| node_b_id | string | Type inferred from 'kite' |
| physical_sector | string | Type inferred from 'kite' |
| cell_id | string | Type inferred from 'kite' |
| local_cell_id | string | Type inferred from 'kite' |
| psc_pci | string | Type inferred from 'kite' |
| rnc | string | Type inferred from 'kite' |
| rnc_id | string | Type inferred from 'kite' |
| lac_tal | string | Type inferred from 'kite' |
| tac | string | Type inferred from 'kite' |
| rac | string | Type inferred from 'kite' |
| ura | string | Type inferred from 'kite' |
| sac | string | Type inferred from 'kite' |
| time_offset | string | Type inferred from 'kite' |
| max_transmit_power_of_cell | string | Type inferred from 'kite' |
| pcpich_rs_power | string | Type inferred from 'kite' |
| antenna_height | string | Type inferred from 'kite' |
| geographic_azimuth | string | Type inferred from 'kite' |
| magnetic_declination | string | Type inferred from 'kite' |
| magnetic_azimuth | string | Type inferred from 'kite' |
| mech_tilt | string | Type inferred from 'kite' |
| elect_tilt | string | Type inferred from 'kite' |
| antenna_count_per_sector | string | Type inferred from 'kite' |
| antenna_model | string | Type inferred from 'kite' |
| beam_width | string | Type inferred from 'kite' |
| root_sequence_idx | string | Type inferred from 'kite' |
| tx_rx | string | Type inferred from 'kite' |
| ept_date | string | Type inferred from 'kite' |
| project | string | Type inferred from 'kite' |
| batch | string | Type inferred from 'kite' |
| update_type | string | Type inferred from 'kite' |
| update_date | string | Type inferred from 'kite' |
| vendor | string | Type inferred from 'kite' |
| cluster | string | Type inferred from 'kite' |
| operador | string | Type inferred from 'kite' |
| tracker | string | Type inferred from 'kite' |
| asl_local | string | Type inferred from 'kite' |
| asl_ift | string | Type inferred from 'kite' |
| nir_ift | string | Type inferred from 'kite' |
| prefix_911 | string | Type inferred from 'kite' |
| prefix_89 | string | Type inferred from 'kite' |
| region_celular | string | Type inferred from 'kite' |
| region_pcs | string | Type inferred from 'kite' |
| municipio | string | Type inferred from 'kite' |
| id_location_sir | string | Type inferred from 'kite' |
| location_sir | string | Type inferred from 'kite' |
| comentario | string | Type inferred from 'kite' |
| cs_pool | string | Type inferred from 'kite' |
| id_country_sir | string | Type inferred from 'kite' |
| country_sir | string | Type inferred from 'kite' |
| ps_pool | string | Type inferred from 'kite' |
| node_b_u2000_ant | string | Type inferred from 'kite' |
| cellname_ant | string | Type inferred from 'kite' |

Las siguientes columnas se agregaron con la finalidad de tener un control en las cargas de ingestion.

| col_name | data_type | comment |
|--------------------|-----------|------------------------------------------|
| filedate | bigint | Type inferred from 'kite' |
| filename | string | Type inferred from 'kite' |
| hash_id | string | Type inferred from 'kite' |
| sourceid | string | Type inferred from 'kite' |
| registry_state | string | Type inferred from 'kite' |
| datasetname | string | Type inferred from 'kite' |
| timestamp | bigint | Type inferred from 'kite' |
| transaction_status | string | Type inferred from 'kite' |

Para mas informacion consultar la siguiente documentacion: [Documentacion EDA EPT_Manager](/RCI_DataAnalysis/eda/EPT_Manager/README.md)

- **[particiones]**
    En la siguiente tabla se enlistan las particiones que contiene la tabla ejecutando el siguiente comando:
    
```
show partitions rci_network_db.tx_ept_lte_outdoor;
```

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|---------|--------|----------|--------|---------------------------------------------------------------------------------------------------|
| 2019 | 1 | 2 | 140910 | 1 | 144.86MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=2 |
| 2019 | 1 | 3 | 140934 | 1 | 144.88MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=3 |
| 2019 | 1 | 4 | 140907 | 1 | 144.85MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=4 |
| 2019 | 1 | 7 | 140904 | 1 | 144.85MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=7 |
| 2019 | 1 | 8 | 140874 | 1 | 144.82MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=8 |
| 2019 | 1 | 10 | 140881 | 1 | 144.83MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=10 |
| 2019 | 1 | 11 | 141714 | 1 | 145.59MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=11 |
| 2019 | 1 | 14 | 141714 | 1 | 145.58MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=14 |
| 2019 | 1 | 15 | 141717 | 1 | 145.59MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=15 |
| 2019 | 1 | 17 | 141868 | 1 | 145.79MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=17 |
| 2019 | 1 | 18 | 141868 | 1 | 145.79MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=18 |
| 2019 | 1 | 21 | 141874 | 1 | 145.80MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=21 |
| 2019 | 1 | 22 | 141955 | 1 | 145.89MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=22 |
| 2019 | 1 | 23 | 141955 | 1 | 145.88MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=23 |
| 2019 | 1 | 24 | 141955 | 1 | 145.88MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=24 |
| 2019 | 1 | 25 | 141963 | 1 | 145.89MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=25 |
| 2019 | 1 | 28 | 141855 | 1 | 145.78MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=28 |
| 2019 | 1 | 29 | 141851 | 1 | 145.78MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=29 |
| 2019 | 1 | 30 | 141851 | 1 | 145.78MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=30 |
| 2019 | 1 | 31 | 141851 | 1 | 145.78MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=1/day=31 |
| 2019 | 2 | 5 | 136892 | 1 | 141.01MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=5 |
| 2019 | 2 | 6 | 137012 | 1 | 141.12MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=6 |
| 2019 | 2 | 7 | 137015 | 1 | 141.18MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=7 |
| 2019 | 2 | 8 | 137015 | 1 | 141.22MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=8 |
| 2019 | 2 | 11 | 137015 | 1 | 141.22MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=11 |
| 2019 | 2 | 12 | 137062 | 1 | 141.26MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=12 |
| 2019 | 2 | 13 | 137073 | 1 | 141.27MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=13 |
| 2019 | 2 | 15 | 137046 | 1 | 141.20MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=15 |
| 2019 | 2 | 18 | 136617 | 1 | 140.79MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=18 |
| 2019 | 2 | 19 | 136443 | 1 | 140.62MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=19 |
| 2019 | 2 | 20 | 136461 | 1 | 140.12MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=20 |
| 2019 | 2 | 21 | 134005 | 1 | 137.65MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=21 |
| 2019 | 2 | 22 | 135585 | 1 | 139.26MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=22 |
| 2019 | 2 | 25 | 135636 | 1 | 139.31MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=25 |
| 2019 | 2 | 26 | 135636 | 1 | 139.36MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=26 |
| 2019 | 2 | 27 | 135582 | 1 | 139.31MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=2/day=27 |
| 2019 | 3 | 1 | 135582 | 1 | 139.31MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=1 |
| 2019 | 3 | 4 | 135633 | 1 | 139.36MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=4 |
| 2019 | 3 | 5 | 136146 | 1 | 139.86MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=5 |
| 2019 | 3 | 6 | 136142 | 1 | 139.86MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=6 |
| 2019 | 3 | 11 | 136156 | 1 | 140.15MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=11 |
| 2019 | 3 | 12 | 136027 | 1 | 140.01MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=12 |
| 2019 | 3 | 13 | 135997 | 1 | 139.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=13 |
| 2019 | 3 | 14 | 135997 | 1 | 139.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=14 |
| 2019 | 3 | 15 | 135716 | 1 | 139.69MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=15 |
| 2019 | 3 | 19 | 135653 | 1 | 139.63MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=19 |
| 2019 | 3 | 20 | 135653 | 1 | 139.63MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=20 |
| 2019 | 3 | 21 | 135841 | 1 | 139.81MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=21 |
| 2019 | 3 | 22 | 135841 | 1 | 139.81MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=22 |
| 2019 | 3 | 25 | 135841 | 1 | 139.81MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=25 |
| 2019 | 3 | 26 | 135884 | 1 | 139.85MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=26 |
| 2019 | 3 | 27 | 136019 | 1 | 139.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=27 |
| 2019 | 3 | 28 | 136016 | 1 | 139.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=28 |
| 2019 | 3 | 29 | 136016 | 1 | 140.02MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/outdoor/year=2019/month=3/day=29 |
| Total |  |  | 7459656 | 54 | 7.49GB |  |  |


```
show partitions rci_network_db.tx_ept_lte_indoor;
```

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|--------|--------|----------|--------|--------------------------------------------------------------------------------------------------|
| 2019 | 1 | 2 | 5026 | 1 | 5.08MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=2 |
| 2019 | 1 | 3 | 5026 | 1 | 5.08MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=3 |
| 2019 | 1 | 4 | 5016 | 1 | 5.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=4 |
| 2019 | 1 | 7 | 5029 | 1 | 5.08MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=7 |
| 2019 | 1 | 8 | 5029 | 1 | 5.08MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=8 |
| 2019 | 1 | 10 | 5030 | 1 | 5.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=10 |
| 2019 | 1 | 11 | 5030 | 1 | 5.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=11 |
| 2019 | 1 | 14 | 5030 | 1 | 5.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=14 |
| 2019 | 1 | 15 | 5030 | 1 | 5.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=15 |
| 2019 | 1 | 17 | 5030 | 1 | 5.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=17 |
| 2019 | 1 | 18 | 5029 | 1 | 5.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=18 |
| 2019 | 1 | 21 | 5029 | 1 | 5.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=21 |
| 2019 | 1 | 22 | 5029 | 1 | 5.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=22 |
| 2019 | 1 | 23 | 5029 | 1 | 5.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=23 |
| 2019 | 1 | 24 | 5029 | 1 | 5.07MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=24 |
| 2019 | 1 | 25 | 5077 | 1 | 5.11MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=25 |
| 2019 | 1 | 28 | 5077 | 1 | 5.11MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=28 |
| 2019 | 1 | 29 | 5077 | 1 | 5.11MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=29 |
| 2019 | 1 | 30 | 5077 | 1 | 5.11MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=30 |
| 2019 | 1 | 31 | 5122 | 1 | 5.16MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=1/day=31 |
| 2019 | 2 | 5 | 5122 | 1 | 5.16MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=5 |
| 2019 | 2 | 6 | 5121 | 1 | 5.16MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=6 |
| 2019 | 2 | 7 | 5121 | 1 | 5.16MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=7 |
| 2019 | 2 | 8 | 5121 | 1 | 5.16MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=8 |
| 2019 | 2 | 11 | 5121 | 1 | 5.16MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=11 |
| 2019 | 2 | 12 | 5121 | 1 | 5.16MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=12 |
| 2019 | 2 | 13 | 5121 | 1 | 5.00MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=13 |
| 2019 | 2 | 15 | 5121 | 1 | 4.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=15 |
| 2019 | 2 | 18 | 5121 | 1 | 4.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=18 |
| 2019 | 2 | 19 | 5121 | 1 | 4.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=19 |
| 2019 | 2 | 20 | 5121 | 1 | 4.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=20 |
| 2019 | 2 | 21 | 5121 | 1 | 4.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=21 |
| 2019 | 2 | 22 | 5121 | 1 | 4.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=22 |
| 2019 | 2 | 25 | 5121 | 1 | 4.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=25 |
| 2019 | 2 | 26 | 5121 | 1 | 4.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=26 |
| 2019 | 2 | 27 | 5121 | 1 | 4.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=2/day=27 |
| 2019 | 3 | 1 | 5121 | 1 | 4.98MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=1 |
| 2019 | 3 | 4 | 4201 | 1 | 4.27MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=4 |
| 2019 | 3 | 5 | 4201 | 1 | 4.25MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=5 |
| 2019 | 3 | 6 | 4201 | 1 | 4.25MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=6 |
| 2019 | 3 | 11 | 4199 | 1 | 4.25MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=11 |
| 2019 | 3 | 12 | 4205 | 1 | 4.27MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=12 |
| 2019 | 3 | 13 | 4205 | 1 | 4.27MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=13 |
| 2019 | 3 | 14 | 4205 | 1 | 4.22MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=14 |
| 2019 | 3 | 15 | 4198 | 1 | 4.24MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=15 |
| 2019 | 3 | 19 | 4198 | 1 | 4.24MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=19 |
| 2019 | 3 | 20 | 4198 | 1 | 4.24MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=20 |
| 2019 | 3 | 21 | 4198 | 1 | 4.22MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=21 |
| 2019 | 3 | 22 | 4198 | 1 | 4.22MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=22 |
| 2019 | 3 | 25 | 4198 | 1 | 4.22MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=25 |
| 2019 | 3 | 26 | 4198 | 1 | 4.22MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=26 |
| 2019 | 3 | 27 | 4198 | 1 | 4.22MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=27 |
| 2019 | 3 | 28 | 4228 | 1 | 4.24MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=28 |
| 2019 | 3 | 29 | 4228 | 1 | 4.25MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/lte/indoor/year=2019/month=3/day=29 |
| Total |  |  | 259366 | 54 | 259.55MB |  |  |


```
show partitions rci_network_db.tx_ept_plan_outdoor;
```

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|--------|--------|----------|--------|----------------------------------------------------------------------------------------------------|
| 2019 | 2 | 6 | 5177 | 1 | 5.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=6 |
| 2019 | 2 | 7 | 5177 | 1 | 5.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=7 |
| 2019 | 2 | 8 | 5177 | 1 | 5.04MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=8 |
| 2019 | 2 | 11 | 5225 | 1 | 5.09MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=11 |
| 2019 | 2 | 12 | 5290 | 1 | 5.15MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=12 |
| 2019 | 2 | 13 | 5290 | 1 | 5.15MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=13 |
| 2019 | 2 | 15 | 5311 | 1 | 5.17MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=15 |
| 2019 | 2 | 18 | 5296 | 1 | 5.16MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=18 |
| 2019 | 2 | 19 | 5284 | 1 | 5.15MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=19 |
| 2019 | 2 | 20 | 5284 | 1 | 5.15MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=20 |
| 2019 | 2 | 21 | 7743 | 1 | 7.61MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=21 |
| 2019 | 2 | 22 | 7743 | 1 | 7.61MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=22 |
| 2019 | 2 | 25 | 7692 | 1 | 7.56MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=25 |
| 2019 | 2 | 26 | 7692 | 1 | 7.56MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=26 |
| 2019 | 2 | 27 | 8022 | 1 | 7.89MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=2/day=27 |
| 2019 | 3 | 1 | 8027 | 1 | 7.89MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=1 |
| 2019 | 3 | 4 | 7958 | 1 | 7.83MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=4 |
| 2019 | 3 | 5 | 6902 | 1 | 6.83MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=5 |
| 2019 | 3 | 6 | 6902 | 1 | 6.83MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=6 |
| 2019 | 3 | 7 | 6908 | 1 | 6.83MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=7 |
| 2019 | 3 | 8 | 6908 | 1 | 6.83MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=8 |
| 2019 | 3 | 11 | 6834 | 1 | 6.76MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=11 |
| 2019 | 3 | 12 | 6658 | 1 | 6.58MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=12 |
| 2019 | 3 | 13 | 6658 | 1 | 6.58MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=13 |
| 2019 | 3 | 14 | 6658 | 1 | 6.58MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=14 |
| 2019 | 3 | 15 | 6658 | 1 | 6.58MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=15 |
| 2019 | 3 | 19 | 6762 | 1 | 6.68MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=19 |
| 2019 | 3 | 20 | 6804 | 1 | 6.73MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=20 |
| 2019 | 3 | 21 | 6394 | 1 | 6.32MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=21 |
| 2019 | 3 | 22 | 6394 | 1 | 6.32MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=22 |
| 2019 | 3 | 25 | 6394 | 1 | 6.32MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=25 |
| 2019 | 3 | 26 | 6321 | 1 | 6.20MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=26 |
| 2019 | 3 | 27 | 6014 | 1 | 5.90MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=27 |
| 2019 | 3 | 28 | 6014 | 1 | 5.90MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=28 |
| 2019 | 3 | 29 | 6014 | 1 | 5.90MB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/outdoor/year=2019/month=3/day=29 |
| Total |  |  | 225585 | 35 | 221.76MB |  |  |


```
show partitions rci_network_db.tx_ept_plan_indoor;
```

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|-------|--------|----------|--------|---------------------------------------------------------------------------------------------------|
| 2019 | 3 | 4 | 326 | 1 | 329.17KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=4 |
| 2019 | 3 | 5 | 326 | 1 | 329.17KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=5 |
| 2019 | 3 | 6 | 326 | 1 | 329.17KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=6 |
| 2019 | 3 | 7 | 326 | 1 | 327.18KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=7 |
| 2019 | 3 | 8 | 326 | 1 | 327.08KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=8 |
| 2019 | 3 | 11 | 319 | 1 | 320.25KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=11 |
| 2019 | 3 | 12 | 319 | 1 | 322.18KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=12 |
| 2019 | 3 | 13 | 319 | 1 | 322.18KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=13 |
| 2019 | 3 | 14 | 319 | 1 | 322.18KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=14 |
| 2019 | 3 | 15 | 340 | 1 | 340.36KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=15 |
| 2019 | 3 | 19 | 328 | 1 | 330.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=19 |
| 2019 | 3 | 20 | 328 | 1 | 330.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=20 |
| 2019 | 3 | 21 | 328 | 1 | 330.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=21 |
| 2019 | 3 | 22 | 328 | 1 | 330.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=22 |
| 2019 | 3 | 25 | 328 | 1 | 330.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=25 |
| 2019 | 3 | 26 | 328 | 1 | 330.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=26 |
| 2019 | 3 | 27 | 328 | 1 | 330.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=27 |
| 2019 | 3 | 28 | 328 | 1 | 330.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=28 |
| 2019 | 3 | 29 | 328 | 1 | 330.37KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/plan/indoor/year=2019/month=3/day=29 |
| Total |  |  | 6198 | 19 | 6.09MB |  |  |

```
show partitions rci_network_db.tx_ept_events_specials;
```

| year | month | day | #Rows | #Files | Size | Format | Location |
|-------|-------|-----|-------|--------|----------|--------|---------------------------------------------------------------------------------------------|
| 2019 | 1 | 2 | 478 | 1 | 489.61KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=2 |
| 2019 | 1 | 3 | 478 | 1 | 489.61KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=3 |
| 2019 | 1 | 4 | 478 | 1 | 489.69KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=4 |
| 2019 | 1 | 7 | 538 | 1 | 547.07KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=7 |
| 2019 | 1 | 8 | 538 | 1 | 547.07KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=8 |
| 2019 | 1 | 10 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=10 |
| 2019 | 1 | 11 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=11 |
| 2019 | 1 | 14 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=14 |
| 2019 | 1 | 15 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=15 |
| 2019 | 1 | 17 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=17 |
| 2019 | 1 | 18 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=18 |
| 2019 | 1 | 21 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=21 |
| 2019 | 1 | 22 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=22 |
| 2019 | 1 | 23 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=23 |
| 2019 | 1 | 24 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=24 |
| 2019 | 1 | 25 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=25 |
| 2019 | 1 | 28 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=28 |
| 2019 | 1 | 29 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=29 |
| 2019 | 1 | 30 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=30 |
| 2019 | 1 | 31 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=1/day=31 |
| 2019 | 2 | 5 | 538 | 1 | 547.05KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=5 |
| 2019 | 2 | 6 | 538 | 1 | 545.01KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=6 |
| 2019 | 2 | 7 | 538 | 1 | 545.01KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=7 |
| 2019 | 2 | 8 | 538 | 1 | 545.01KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=8 |
| 2019 | 2 | 11 | 538 | 1 | 545.01KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=11 |
| 2019 | 2 | 12 | 538 | 1 | 545.01KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=12 |
| 2019 | 2 | 13 | 538 | 1 | 545.01KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=13 |
| 2019 | 2 | 15 | 538 | 1 | 545.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=15 |
| 2019 | 2 | 18 | 538 | 1 | 545.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=18 |
| 2019 | 2 | 19 | 538 | 1 | 545.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=19 |
| 2019 | 2 | 20 | 538 | 1 | 545.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=20 |
| 2019 | 2 | 21 | 538 | 1 | 545.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=21 |
| 2019 | 2 | 22 | 538 | 1 | 545.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=22 |
| 2019 | 2 | 25 | 538 | 1 | 545.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=25 |
| 2019 | 2 | 26 | 538 | 1 | 545.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=26 |
| 2019 | 2 | 27 | 538 | 1 | 545.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=2/day=27 |
| 2019 | 3 | 1 | 538 | 1 | 545.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=1 |
| 2019 | 3 | 4 | 538 | 1 | 545.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=4 |
| 2019 | 3 | 5 | 538 | 1 | 545.99KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=5 |
| 2019 | 3 | 6 | 538 | 1 | 545.99KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=6 |
| 2019 | 3 | 7 | 538 | 1 | 545.99KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=7 |
| 2019 | 3 | 8 | 538 | 1 | 545.99KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=8 |
| 2019 | 3 | 11 | 538 | 1 | 545.99KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=11 |
| 2019 | 3 | 12 | 538 | 1 | 545.99KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=12 |
| 2019 | 3 | 13 | 538 | 1 | 545.99KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=13 |
| 2019 | 3 | 14 | 486 | 1 | 493.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=14 |
| 2019 | 3 | 15 | 486 | 1 | 493.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=15 |
| 2019 | 3 | 19 | 486 | 1 | 493.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=19 |
| 2019 | 3 | 20 | 486 | 1 | 493.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=20 |
| 2019 | 3 | 21 | 486 | 1 | 493.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=21 |
| 2019 | 3 | 22 | 486 | 1 | 493.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=22 |
| 2019 | 3 | 25 | 486 | 1 | 493.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=25 |
| 2019 | 3 | 26 | 486 | 1 | 493.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=26 |
| 2019 | 3 | 27 | 486 | 1 | 493.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=27 |
| 2019 | 3 | 28 | 486 | 1 | 493.00KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=28 |
| 2019 | 3 | 29 | 486 | 1 | 492.87KB | AVRO | hdfs://attdatalakehdfs/data/RCI/stg/hive/staging/ept_manager/event/year=2019/month=3/day=29 |
| Total |  |  | 29376 | 56 | 29.13MB |  |  |



## Componentes del procesos de ingestion

1. **Ingestion y Serialización via NiFi**

    ![EPT Manager NiFi General View][img1]   
    *Pipeline General __EPT Manager__*

    ![EPT Manager NiFi Main View][img2]                             
    *Pipeline Main __EPT Manager__*

    ![EPT Manager NiFi Flow View][img3]      
    *Pipeline Flow __EPT Manager__*

    ![EPT Manager NiFi Detail View][img4]      
    *Pipeline Esquema Avro __EPT Manager__*

    ![EPT Manager NiFi Detail View][img5]      
    *Pipeline Cifras Control __EPT Manager__*

2. **Reglas de estandarizacion del esquema**

    * Sobre el esquema se eliminaron caracteres para que se generara correctamente el esquema del archivo avro con la siguiente expresion regular:
    
     ```
     Valor de Busqueda: (?s)(^[^\n]*)(.*$)
     Expresion regular a ejecutar: ${'$1':replace(" ","_"):replace("(",""):replace(")",""):replace("-","_"):replace("/","_"):replace("|\"\"|","|\"Node_B_ID\"|"):replace("&",""):replace("911","Prefix_911"):replace("89","Prefix_89"):replace("Node_B_U2000_Ant","Node_B_U2000_Anterior"):replace("CellName_Ant","CellName_Anterior")}$2
     ```
   
3. **Framework de Ingestión Automatizado**

    * Parámetros del proceso de ingestion:

| Parámetro | Valor | Descripción|
| ---------- | ---------- | ---------- |
| parametro_01   | 94   | Valor de correspondiente al flujo de EPT Manager **tx_ept_lte_outdoor** |
| parametro_01   | 95   | Valor de correspondiente al flujo de EPT Manager **tx_ept_lte_indoor** |
| parametro_01   | 96   | Valor de correspondiente al flujo de EPT Manager **tx_ept_plan_outdoor** |
| parametro_01   | 97   | Valor de correspondiente al flujo de EPT Manager **tx_ept_plan_indoor** |
| parametro_01   | 98   | Valor de correspondiente al flujo de EPT Manager **tx_ept_events_especials** |

   * Sintaxis del comando de ejecucion del proceso de automatización:
   
     ```
     sh rci_ingesta_generacion_avro.sh {parametro_01}
     ```
   
   * El siguiente comando es un ejemplo para ejecutar el proceso de automatización: 
    
     ```
     sh rci_ingesta_generacion_avro.sh 94
     ```

## Referencias al Framework de Ingestion

[Framework de Ingestion](../Globales/ArquitecturaFrameworkIngestion/readme.md)

## Codigo Fuente Local

- [Codigo NiFi - NFR](NFR/)

## Codigo Fuente Globales

- [Codigo NiFi](../Globales/NIFICustomProcessorXLSX/README.md)
- [Codigo Spark](../Globales/SparkAxity/README.md)
- [Codigo Kite](../Globales/attdlkrci/readme.md)

##### [Ir a Inicio](#main)

---

 [img1]: images/ept-manager-nifi-01.png "EPT Manager NiFi General View"
 [img2]: images/ept-manager-nifi-02.png "EPT Manager NiFi Main View"
 [img3]: images/ept-manager-nifi-03.png "EPT Manager NiFi Flow View"
 [img4]: images/ept-manager-nifi-04.png "EPT Manager NiFi Detail View"
 [img5]: images/ept-manager-nifi-05.png "EPT Manager NiFi Detail View"
 