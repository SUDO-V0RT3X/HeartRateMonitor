There seems to be some existing modules for heart rate monitoring. The HKD AD8232 ECG PULSE HEART SENSOR from Communica (https://www.communica.co.za/products/hkd-ad8232-ecg-pulse-heart-senso?variant=52337050485036) costs R130.43 at the time of writing this, which is somehow cheaper than the SPF HEART RATE MONITOR - AD8232 from the same company (<https://www.communica.co.za/products/spf-heart-rate-monitor-ad8232?variant=17184685097033) which costs R415. This is quite strange

The AD8232 is built with an instrumentation amplifier, a few amplifiers, come comparators and a few other things. Further information can be found in the datasheet.

Build such a chip from scratch should not be too complex. An instrumentation amplifier's pupose is to amplify the mV range differential signals and reject the large background noise. 
After the IA, the signal can be amplified further.

YouTube videos with some decent contnet:
1. https://youtu.be/5YxrpcqkTYA?si=MjpXJfiADk2nOV0v
2. https://youtu.be/Ilv_VNvS42w?si=rzwtEUj45PeVK31_
3. https://youtu.be/-G3z9fvQnuw?si=vS8afweoRCjJgYn8
4. https://youtu.be/AfirWls9Sys?si=bxoBOUqJR-nA8x_0
5. https://youtu.be/nIeipbjleuY?si=R629lEGSQSImLTJj
6. https://youtu.be/sP_-f5nsOEo?si=MpwHychBWEMl0BsE
7. https://youtu.be/7fuj2mdduKQ?si=k1g-MoNYCvvxFcZT
8. https://youtu.be/sIrTu5LuSZw?si=qF9GimzcYU1RpjfZ

Also useful:
1. https://swharden.com/blog/2016-08-08-diy-ecg-with-1-op-amp/


Research paper:
https://pmc.ncbi.nlm.nih.gov/articles/PMC9185322/
To note: various circuits exist for different types of electrodes (dry, wet, gel, etc.)
This must be taken into account also.
