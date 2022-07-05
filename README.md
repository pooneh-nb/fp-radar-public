# FP-Radar
Artifact release for ourPrivacy Enhancing Technologies Symposium, 2022  paper entitled FP-Radar: Longitudinal Measurement and Early Detection of Browser Fingerprinting

# Reference
**FP-Radar: Longitudinal Measurement and Early Detection of Browser Fingerprinting** Pouneh Nikkhah Bahrami*, Umar Iqbal, and Zubair Shafiq
Privacy Enhancing Technologies Symposium (PETS), 2022

**Abstract**-- Browser fingerprinting is a stateless tracking technique that aims to combine information exposed by multiple different web APIs to create a unique identifier for tracking users across the web. Over the last decade, trackers have abused several existing and newly proposed web APIs to further enhance the browser fingerprint. Existing approaches are limited to detecting a specific fingerprinting technique(s) at a particular point in time. Thus, they are unable to systematically detect novel fingerprinting techniques that abuse different web APIs. In this paper, we propose FP-Radar, a machine learning approach that leverages longitudinal measurements of web API usage on top-100K websites over the last decade for early detection of new and evolving browser fingerprinting techniques. The results show that FP-Radar is able to early detect the abuse of newly introduced properties of already known (e.g., WebGL, Sensor) and as well as previously unknown (e.g., Gamepad, Clipboard) APIs for browser fingerprinting.
To the best of our knowledge, FP-Radar is the first to
detect the abuse of the Visibility API for ephemeral
fingerprinting in the wild.
