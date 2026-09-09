There seems to be some existing modules for heart rate monitoring. The HKD AD8232 ECG PULSE HEART SENSOR from Communica (https://www.communica.co.za/products/hkd-ad8232-ecg-pulse-heart-senso?variant=52337050485036) costs R130.43 at the time of writing this, which is somehow cheaper than the SPF HEART RATE MONITOR - AD8232 from the same company (<https://www.communica.co.za/products/spf-heart-rate-monitor-ad8232?variant=17184685097033) which costs R415. This is quite strange

The AD8232 is built with an instrumentation amplifier, a few amplifiers, come comparators and a few other things. Further information can be found in the datasheet.

Build such a chip from scratch should not be too complex. An instrumentation amplifier's pupose is to amplify the mV range differential signals and reject the large background noise. 
After the IA, the signal can be amplified further.
