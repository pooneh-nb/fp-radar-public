from myCodes.AST import utilities
import os
import jsbeautifier
import pandas as pd


def api_analysis(fp_js_files_years, out_dir, keyword_list, id_domain):

    #keyword_list = ["hardwareConcurrency"]

    script_api_key = {}
    years = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
    """for year in years:
        files = utilities.get_files_in_a_directory(os.path.join(fp_js_files_years, year, "api_features"))
        for fp_script in files:
            script_name = fp_script.split('/')[-1]
            script_context = utilities.read_list_compressed(fp_script)
            for apikw in keyword_list:
                if apikw in script_context:
                    if apikw in script_api_key.keys():
                        script_api_key[apikw].append(script_name)
                    else:
                        script_api_key[apikw] = []
                        script_api_key[apikw].append(script_name)

    #utilities.write_json(os.path.join(out_dir, script_name), script_context)
    utilities.write_json(os.path.join(out_dir, "key_list"), script_api_key)"""

    api_dict = {}
    for year in years:
        files = utilities.get_files_in_a_directory(os.path.join(fp_js_files_years, year, "api_features"))
        for fp_script in files:
            script_name = fp_script.split('/')[-1].split('.')[0]
            script_context = utilities.read_list_compressed(fp_script)
            script_entropy = set()
            for apikw in keyword_list:
                if apikw in script_context:
                    script_entropy.add(apikw)
            if len(script_entropy) >= 4:
                url_id = script_name.split('|')[-1].split('.')[0]
                script_year = script_name.split('|')[-2][0:4]
                top_domain = id_domain[url_id]
                if url_id not in api_dict.keys():
                    api_dict[url_id] = {"year": [script_year], "file_name": [script_name], "topDomain": [top_domain], "script_entropy": [list(script_entropy)]}
                    wrirejs(script_name, out_dir)
                else:
                    if script_year not in api_dict[url_id]["year"]:
                        api_dict[url_id]["year"].append(script_year)
                        api_dict[url_id]["file_name"].append(script_name)
                        api_dict[url_id]["script_entropy"].append(list(script_entropy))
                        wrirejs(script_name, out_dir)
                #print(script_name)
                #print(script_entropy)
    utilities.write_json(os.path.join(out_dir, "dictionary.json"), api_dict)
    for url_id, values in api_dict.items():
        print(url_id, values)


def non_fp_api_analysis(non_fp_js_files_years, out_dir, keyword_list):

    years = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]

    api_dict = {}
    for year in years:
        files = utilities.get_files_in_a_directory(os.path.join(non_fp_js_files_years, year, "api_features"))
        for fp_script in files:
            script_name = fp_script.split('/')[-1].split('.')[0]
            script_context = utilities.read_list_compressed(fp_script)
            script_entropy = set()
            for apikw in keyword_list:
                if apikw in script_context:
                    script_entropy.add(apikw)
            if len(script_entropy) >= 1:
                url_id = script_name.split('|')[-1].split('.')[0]
                script_year = script_name.split('|')[-2][0:4]
                if url_id not in api_dict.keys():
                    api_dict[url_id] = {"year": [script_year], "file_name": [script_name],
                                        "script_entropy": [list(script_entropy)]}
                    #wrirejs(script_name, out_dir)
                else:
                    if script_year not in api_dict[url_id]["year"]:
                        api_dict[url_id]["year"].append(script_year)
                        api_dict[url_id]["file_name"].append(script_name)
                        api_dict[url_id]["script_entropy"].append(list(script_entropy))
                # print(script_name)
                # print(script_entropy)
    utilities.write_json(os.path.join(out_dir, "dictionary.json"), api_dict)
    for url_id, values in api_dict.items():
        print(url_id, values)


def jsreader(fine_name):
    script_file = utilities.read_dill_compressed(os.path.join
                                                 ("/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files"
                                                  "/fp_javascripts", fine_name))
    print(jsbeautifier.beautify((script_file)))


def wrirejs(script_name, outdir):
    script_file = utilities.read_dill_compressed(os.path.join
                                                 ("/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files"
                                                  "/fp_javascripts", script_name))
    script_context = jsbeautifier.beautify((script_file))
    utilities.write_content(os.path.join(outdir, script_name + ".js"), script_context)


def create_id_topdomain():
    all_fp_3rdparties = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/third_parties/all_3rdparty_fp_script_urls.json")
    id_domain = {}
    for hash, value in all_fp_3rdparties.items():
        id_domain[str(value["url_id"])] = value["script_url"]
    return id_domain


def main():
    fp_js_files_years = "/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/fp_files"
    non_fp_js_files_years = "/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/non_fp_files"
    out_dir = "/home/c6/Desktop/OpenWPM/jsons/script_analysis/navigator"
    out_dir_non_fp = "/home/c6/Desktop/OpenWPM/jsons/script_analysis/web_worker/non_fp"

    push_api_list = """["pushManager", "getSubscription", "Push_API", "PushSubscriptionOptions", "PushSubscription",
                    "PushManager", "registrations", "subscriptionId", "expirationTime",
                    "supportedContentEncodings", "getSubscription", "endpoint", "hasPermission",
                    "userVisibleOnly", "PushPermissionStatus", "permissionState", "applicationServerKey",
                    "Service_Worker_API", "getRegistration", "getRegistrations", "subscribe"]"""
    battery_status_keywords = ["BatteryManager", "charging", "chargingtimechange", "dischargingTime", "chargingTime",
                               "chargingchange", "level", "levelchange", "dischargingtimechange", "levelchange", "battery",
                               "getBattery", "level", "mozBattery", "dischargingTime"]
    navigator_keywords = ["vendor", "standalone", "NavigatorLanguage", "webdriver", "doNotTrack", "vendorSub", "oscpu",
                          "registerProtocolHandler", "suffixes", "taintEnabled", "languages", "cookieEnabled", "Mozilla",
                          "enabledPlugin", "productSub", "deviceMemory", "product", "appVersion", "platform", "plugins",
                          "appName", "hardwareConcurrency", "appCodeName", "PluginArray", "MimeType", "javaEnabled",
                          "buildID"]

    networkInformation_keywords = ["effectiveType", "downlinkMax", "rtt", "NetworkInformation", "saveData", "downlink",
                                   "connection", "mozConnection", "webkitConnection"]
    geolocation_keywords = ["watchPosition", "geolocation", "clearWatch", "speed", "altitude", "latitude", "TIMEOUT",
                            "longitude", "altitudeAccuracy", "PERMISSION_DENIED", "POSITION_UNAVAILABLE"]
    payment_keywords = ["requestId", "amount", "retry", "organization", "phone", "PaymentAddress", "shippingAddress",
                        "city", "country", "currency", "cardholderName", "cardNumber", "payer", "billingAddress",
                        "languageCode", "paymentRequestOrigin", "payerPhone", "payerName", "postalCode",
                        "hasEnrolledInstrument", "CanMakePaymentEvent", "methodData", "ServiceWorker", "scriptURL",
                        "IndexedDB", "enableHighAccuracy", "maximumAge"]
    longTask_keywords = ["containerType", "containerId", "attribution", "TaskAttributionTiming", "PerformanceLongTaskTiming"]
    vibrate_list = ["vibrate", "Vibration"]
    Web_storage_API = ["Storage", "localStorage", "sessionStorage", "storageArea", "setItem"]
    Navigator_list = ["taintEnabled", "PluginArray", "appVersion", "Mozilla", "enabledPlugin", "hardwareConcurrency",
                      "MimeType", "javaEnabled", "suffixes", "product", "appCodeName", "plugins", "languages",
                      "platform", "NavigatorLanguage", "appName"]
    webgl_list = ["WEBGL_compressed_texture_astc", "EXT_disjoint_timer_query", "compileShader", "WEBGL_debug_shaders",
     "EXT_shader_texture_lod", "useProgram", "WEBGL_lose_context", "linkProgram", "EXT_blend_minmax",
     "EXT_color_buffer_half_float", "getProgramParameter", "drawArrays", "Uint32Array",
     "isBuffer", "attachShader", "getUniformLocation", "createQuery", "bindBuffer", "WEBGL_debug_renderer_info",
     "OES_texture_half_float_linear", "MAX_TEXTURE_MAX_ANISOTROPY_EXT", "EXT_frag_depth", "webgl",
    "MAX_COLOR_ATTACHMENTS_WEBGL", "OES_element_index_uint", "WEBGL_color_buffer_float",
     "WebGLRenderingContext", "ANGLE_instanced_arrays", "WEBGL_depth_texture", "enableVertexAttribArray", "depthFunc",
     "shaderSource", "vertexAttribPointer", "clearColor", "WebGLContextEvent", "OES_vertex_array_object",
     "getSupportedExtensions", "WEBGL_compressed_texture_s3tc", "OES_standard_derivatives", "enable",
     "WebGL2RenderingContext", "OES_texture_half_float", "rangeMax", "EXT_texture_filter_anisotropic",
     "FRAGMENT_SHADER_DERIVATIVE_HINT_OES", "FLOAT", "OES_texture_float_linear", "getAttribLocation", "precision",
     "MAX_DRAW_BUFFERS_WEBGL", "WEBGL_draw_buffers", "bufferData", "getShaderPrecisionFormat", "getContextAttributes",
     "rangeMin", "statusMessage", "getExtension", "EXT_sRGB", "createShader", "WEBGL_compressed_texture_atc", "getError",
     "WEBGL_compressed_texture_etc1", "createProgram", "viewport", "OES_texture_float", "lineWidth"]

    resource_timing = ["redirectEnd", "getEntries", "loadEventStart", "initiatorType", "unloadEventStart", "connectStart", "timing",
                       "transferSize", "domContentLoadedEventStart", "getEntriesByType", "navigationStart", "responseStart",
                       "domContentLoadedEventEnd", "getEntriesByName",  "responseEnd", "domComplete", "clearMarks",
                       "serverTiming", "domainLookupStart", "back_forward",  "requestStart", "secureConnectionStart",
                       "clearMeasures", "loadEventEnd", "redirectCount", "encodedBodySize",  "decodedBodySize",
                       "paint", "unloadEventEnd", "domLoading", "domainLookupEnd", "mark", "nextHopProtocol",
                       "resource", "navigation", "redirectStart", "Performance", "measure", "connectEnd", "fetchStart",
                       "workerStart", "domInteractive", "entryType"]
    History_list = ["go", "history", "History", "pushState"]
    geolocation = ["TIMEOUT", "geolocation", "longitude", "altitude", "PERMISSION_DENIED", "clearWatch",
                   "POSITION_UNAVAILABLE", "latitude", "speed", "watchPosition", "altitudeAccuracy"]
    Web_Workers_list = ["applicationCache", "Worker", "responseXML", "Gecko", "unhandledrejection", "importScripts",
                        "Worklet", "btoa", "isSecureContext", "online", "ApplicationCache"]
    Permission_list = ["denied", "revoke"]
    xmlhttprequest = ["responseXML", "statusText", "responseText", "getAllResponseHeaders", "responseURL",
                      "overrideMimeType", "XMLHttpRequest", "responseType"]
    server_sent_events = ["EventSource"]
    Page_Visibility_list = ["prerender", "visibilityState", "focused", "DeviceOrientationEvent", "DeviceMotionEvent"]
    Sensors = ["accelerationIncludingGravity", "alpha", "DeviceOrientationEvent", "DeviceMotionEvent",
               "gamma", "acceleration","illuminance", "AmbientLightSensor", "sensor", "Accelerometer", "Gyroscope", "magnetometer"]
    URL_API_list = ["createObjectURL", "revokeObjectURL", "URL"]
    Channel_Messaging_list = ["port2", "ports", "MessagePort", "MessageChannel", "port1"]
    XMLSerializer = ["serializeToString", "XMLSerializer"]
    Mouse = ["deltaZ", "deltaX", "deltaY", "mousewheel", "wheelDelta", "wheelDeltaY", "wheelDeltaX", "DOMMouseScroll",
             "movementY", "movementX", "scrollY", "scrollX", "dblclick", "click", "DOMMouseScroll",
             "TouchEvent", "touchenter", "touchleave", "ontouchstart", "DOMMouseScroll",
             "onmousemove", "mousemove", "mousedown", "mouseup", "offsetX", "offsetY", "ScreenX", "ScreenY",
             "pageX", "pageY", "offsetX", "offsetY", "clientX", "clientY", "radiusX", "radiusY",
             "initMouseEvent", "requestPointerLock"]
    Pointer_Lock_List = ["requestPointerLock"]
    FileReader = ["FileReaderSync", "readAsText", "readAsArrayBuffer", "FileReader"]
    HTMLIFrameElement = ["allowfullscreen", "HTMLIFrameElement", "frameBorder", "sandbox", "srcdoc", "marginHeight", "marginWidth"]
    EventListeners = ["UIEvent", "newURL", "inputType", "oldURL", "InputEvent", "sample", "InstallTrigger", "DOMNodeInsertedIntoDocument", "statusCode",
                      "lengthComputable", "handleEvent", "colno", "documentURI", "lineno", "ErrorEvent"]
    IndexedDB_list = ["objectStoreNames", "bound", "IDBDatabase", "transaction", "IndexedDB", "objectStore", "IDBTransaction",
                      "indexedDB", "IDBRequest", "onsuccess", "cmp", "storeName", "createObjectStore", "onupgradeneeded",
                      "keyPath", "setVersion", "lower", "IDBKeyRange", "deleteDatabase"]
    Touch_events_list = ["rotationAngle", "ontouchstart", "force", "TouchEvent", "radiusX", "radiusY",
                         "touchenter", "touchleave", "ontouchstart", "TouchEvent"]
    Storage_List = ["persist", "storage"]
    Web_Crypto_list = ["CryptoKey", "subtle", "salt", "getRandomValues", "decrypt", "encrypt", "crypto"]
    HTML_Drag_and_Drop_list = ["dragstart", "dragover", "dragleave", "dragenter", "drag", "dragend"]
    File_and_Directory_Entries_list = ["formmethod", "readwrite", "errorCallback", "isDirectory", "fullPath", "radio",
                                       "successCallback", "checkbox", "isFile", "TEMPORARY", "PERSISTENT",
                                       "createWriter", "formnovalidate", "copyTo", "requestFileSystem", "setSelectionRange"]
    Streams_list = ["ReadableStream", "byteLength", "WritableStream", "getReader", "respond", "enqueue", "highWaterMark"]
    Media_Streams_list = ["CanvasCaptureMediaStreamTrack", "constraint", "latency", "mozGetUserMedia", "enumerateDevices",
                          "MediaStream", "cursor", "facingMode", "OverconstrainedError", "getAudioTracks", "getSupportedConstraints",
                          "getVideoTracks", "groupId", "getTracks", "getUserMedia", "MediaDevices", "ideal", "MediaStreamTrack"]
    Fullscreen_API = ["msExitFullscreen", "mozRequestFullScreen", "mozCancelFullScreen", "requestFullscreen",
                      "exitFullscreen", "webkitIsFullScreen", "msFullscreenElement", "mozFullScreen", "fullscreen"]
    Gamepad_list =["Gamepad", "getGamepads", "webkit", "mapping"]
    CSS_Painting_API = ["devicePixelRatio"]
    CSS_T_Object_Model = ["itemRef", "onorientationchange", "movementX", "rules", "pixelDepth", "contextMenu",
                          "touchenter", "availWidth", "addListener", "colorDepth", "initMouseEvent", "CSSRuleList",
                          "movementY", "unit", "propertyName", "insertRule", "Screen", "touchleave", "isContentEditable",
                           "offsetWidth", "outerText", "addRule", "availHeight", "mozOrientation", "currentSrc",
                          "offsetHeight", "availLeft", "availTop", "deleteRule", "sub"]
    Clipboard_API = ["copy", "clipboardData", "paste"]
    Web_Audio_list = ["onaudioprocess", "createDynamicsCompressor", "AudioContext", "createOscillator", "baseLatency",
                      "numberOfChannels", "numberOfInputs", "inputBuffer", "createMediaStreamSource", "getChannelData",
                      "OfflineAudioContext", "startRendering", "numberOfOutputs", "ratio", "threshold", "channelCountMode",
                      "buffer", "renderedBuffer", "gain", "AudioWorkletNode", "setTargetAtTime", "setValueAtTime",
                      "dopplerFactor", "audioWorklet", "knee", "attack", "createGain", "AudioBuffer", "ChannelMergerNode",
                      "reduction", "listener", "channelInterpretation", "maxChannelCount", "createScriptProcessor",
                      "getFloatFrequencyData", "createAnalyser", "speedOfSound", "frequencyBinCount", "audio",
                      "AudioWorklet"]
    Canvas_List = ["getContext", "HTMLCanvasElement", "arc", "save", "alphabetic", "getImageData", "isPointInPath",
                   "font", "mozCaptureStream", "lineDashOffset", "lineCap", "drawImage","quadraticCurveTo", "stroke",
                   "addColorStop", "shadowOffsetY", "imageSmoothingEnabled", "strokeStyle", "canvas", "fillText",
                   "fillStyle", "png", "shadowOffsetX", "globalCompositeOperation", "shadowBlur", "beginPath",
                   "textBaseline", "evenodd", "createRadialGradient", "shadowColor", "closePath", "toBlob",
                   "strokeText", "toDataURL", "captureStream", "rect", "fillRect", "bezierCurveTo"]
    Resource_Timing_list = ["redirectEnd", "getEntries", "loadEventStart", "initiatorType", "unloadEventStart",
                            "connectStart", "timing", "transferSize", "domContentLoadedEventStart", "getEntriesByType",
                            "navigationStart", "responseStart", "domContentLoadedEventEnd", "getEntriesByName",
                            "responseEnd", "domComplete", "clearMarks", "serverTiming", "domainLookupStart", "back_forward",
                            "requestStart", "secureConnectionStart", "clearMeasures", "loadEventEnd", "redirectCount",
                            "encodedBodySize", "decodedBodySize", "paint", "unloadEventEnd", "domLoading", "domainLookupEnd",
                            "mark", "nextHopProtocol", "resource", "navigation", "redirectStart", "Performance", "measure",
                            "connectEnd", "fetchStart", "workerStart", "domInteractive", "entryType"]
    Network_Information = ["downlink", "saveData", "rtt", "effectiveType", "NetworkInformation", "downlinkMax"]

    offscreen = ["worker", "OffscreenCanvas", "canvas", "postMessage"]

    id_domain = create_id_topdomain()
    api_analysis(fp_js_files_years, out_dir, navigator_keywords, id_domain)
    #non_fp_api_analysis(non_fp_js_files_years, out_dir_non_fp, Gamepad_list)
    #non_fp_analysis()
    # battery : yes|55OHGA5TALHVIZU32UVBAX5DSOUZOWOJ|20181028|2250"
    # navigator : "yes|PHTTOUGX44NEQV2DCZ33GL5TMLF3AX5S|20191206|9191"
    # network_Information : yes|V25IQD6MUV5QBHHLUOWQNHCGO66T3T4O|20180624|9379
    # geolocation: yes|0eb7b19757ace712dce0bd968db99bb6f7792be6|20170123|11743
    # payment: yes|2RM5OWWFJZQDKTRWRK6RSL6CP7GUN3GV|20191005|1587
    #jsreader("yes|GSQDMBR7ZLUINZPVHAQ4COYXQNOS2L3S|20190620|16153")


if __name__ == '__main__':
    main()
