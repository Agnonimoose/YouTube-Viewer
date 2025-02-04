import playwright
import user-agents
const uuid = require('uuid')
const tmp = require('tmp-promise')

UINT32_MAX = (2 ** 32) - 1
WEBGL_RENDERERS = ['ANGLE (NVIDIA Quadro 2000M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro K420 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA Quadro 2000M Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA Quadro K2000M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Family Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon HD 3800 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics 4000 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics 4000 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (AMD Radeon R9 200 Series Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Family Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Family Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics 4000 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics 3000 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Mobile Intel(R) 4 Series Express Chipset Family Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) G33/G31 Express Chipset Family Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (Intel(R) Graphics Media Accelerator 3150 Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (Intel(R) G41 Express Chipset Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 6150SE nForce 430 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics 4000)', 'ANGLE (Mobile Intel(R) 965 Express Chipset Family Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Family)', 'ANGLE (NVIDIA GeForce GTX 760 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 760 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 760 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (AMD Radeon HD 6310 Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Graphics Media Accelerator 3600 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) G33/G31 Express Chipset Family Direct3D9 vs_0_0 ps_2_0)', 'ANGLE (AMD Radeon HD 6320 Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) G33/G31 Express Chipset Family (Microsoft Corporation - WDDM 1.0) Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (Intel(R) G41 Express Chipset)', 'ANGLE (ATI Mobility Radeon HD 5470 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Q45/Q43 Express Chipset Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 310M Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) G41 Express Chipset Direct3D9 vs_3_0 ps_3_0)', 'ANGLE (Mobile Intel(R) 45 Express Chipset Family (Microsoft Corporation - WDDM 1.1) Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GT 440 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon HD 4300/4500 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 7310 Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics)', 'ANGLE (Intel(R) 4 Series Internal Chipset Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon(TM) HD 6480G Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon HD 3200 Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 7800 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) G41 Express Chipset (Microsoft Corporation - WDDM 1.1) Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 210 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GT 630 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 7340 Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) 82945G Express Chipset Family Direct3D9 vs_0_0 ps_2_0)', 'ANGLE (NVIDIA GeForce GT 430 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 7025 / NVIDIA nForce 630a Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Q35 Express Chipset Family Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (Intel(R) HD Graphics 4600 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 7520G Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD 760G (Microsoft Corporation WDDM 1.1) Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GT 220 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 9500 GT Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Family Direct3D9 vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Graphics Media Accelerator HD Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 9800 GT Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Q965/Q963 Express Chipset Family (Microsoft Corporation - WDDM 1.0) Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (NVIDIA GeForce GTX 550 Ti Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Q965/Q963 Express Chipset Family Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (AMD M880G with ATI Mobility Radeon HD 4250 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 650 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Mobility Radeon HD 5650 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon HD 4200 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 7700 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) G33/G31 Express Chipset Family)', 'ANGLE (Intel(R) 82945G Express Chipset Family Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (SiS Mirage 3 Graphics Direct3D9Ex vs_2_0 ps_2_0)', 'ANGLE (NVIDIA GeForce GT 430)', 'ANGLE (AMD RADEON HD 6450 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon 3000 Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) 4 Series Internal Chipset Direct3D9 vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Q35 Express Chipset Family (Microsoft Corporation - WDDM 1.0) Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (NVIDIA GeForce GT 220 Direct3D9 vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 7640G Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD 760G Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 6450 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GT 640 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 9200 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GT 610 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 6290 Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Mobility Radeon HD 4250 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 8600 GT Direct3D9 vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon HD 5570 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 6800 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) G45/G43 Express Chipset Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon HD 4600 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA Quadro NVS 160M Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics 3000)', 'ANGLE (NVIDIA GeForce G100)', 'ANGLE (AMD Radeon HD 8610G + 8500M Dual Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Mobile Intel(R) 4 Series Express Chipset Family Direct3D9 vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 7025 / NVIDIA nForce 630a (Microsoft Corporation - WDDM) Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Q965/Q963 Express Chipset Family Direct3D9 vs_0_0 ps_2_0)', 'ANGLE (AMD RADEON HD 6350 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon HD 5450 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 9500 GT)', 'ANGLE (AMD Radeon HD 6500M/5600/5700 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Mobile Intel(R) 965 Express Chipset Family)', 'ANGLE (NVIDIA GeForce 8400 GS Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Direct3D9 vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 560 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GT 620 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 660 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon(TM) HD 6520G Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GT 240 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 8240 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA Quadro NVS 140M)', 'ANGLE (Intel(R) Q35 Express Chipset Family Direct3D9 vs_0_0 ps_2_0)']

def getBrowserfingerprint(buid, emulateFlag = 'desktop'):
     generateUserAgent = new UserAgent({
      deviceCategory: emulateFlag,
    })
    fingerprints = Array(1000).fill().map(() => generateUserAgent())

    WEBGL_PARAMETER = {
      "WEBGL_VENDOR": 'Google Inc.',
      "WEBGL_RENDERER": WEBGL_RENDERERS[Math.floor(Math.random() * WEBGL_RENDERERS.length)],
    }

    const fingerprint = Object.assign(fingerprints[Math.floor(Math.random() * fingerprints.length)].data, WEBGL_PARAMETER)

    const buidHash = crypto.createHash('sha512').update(buid).digest()
    fingerprint.BUID = buidHash.toString('base64')

    fingerprint.random = (index) => {
      const idx = index % 124
      if idx < 62) return buidHash.readUInt32BE(idx) / UINT32_MAX
      return buidHash.readUInt32LE(idx - 62) / UINT32_MAX
    }
    return fingerprint
}


async def cloak(page, fingerprint, {
    minWidth = 1280,
    minHeight = 1024,
  } = {}:
    console.debug(`fingerprint-webgl-vendor-${fingerprint.WEBGL_VENDOR}`)
    console.debug(`fingerprint-webgl-renderer-${fingerprint.WEBGL_RENDERER}`)
    console.debug(`fingerprint-ua-ua-${fingerprint.userAgent}`)
    console.debug(`fingerprint-ua-platform-${fingerprint.platform}`)
    console.debug(`fingerprint-deviceCategory-${fingerprint.deviceCategory}`)
    console.debug(`fingerprint-viewportHeight-${fingerprint.viewportHeight}`)
    console.debug(`fingerprint-viewportWidth-${fingerprint.viewportWidth}`)


    const LOG_OVERRIDE = True

    if LOG_OVERRIDE:
      await page.on('console', (msg) => {
        if msg and msg.text:
          if typeof msg.text is 'function':
            debugConsole('PAGE LOG:', msg.text())
          else:
            debugConsole('PAGE LOG:', msg.text)

        else:
          debugConsole('PAGE LOG:', msg)

      })
      await page.on('pageerror', (err) => debug('PAGE ERR:', err))


    const DIMENSION = {
      isLandscape: True,
      width: minWidth > fingerprint.viewportWidth ? minWidth : (parseInt(minWidth + (fingerprint.random(0)
        * (fingerprint.screenWidth - minWidth)), 10)),
      height: minHeight > fingerprint.viewportHeight ? minHeight : (parseInt(minHeight + (fingerprint.random(1)
        * (fingerprint.screenHeight - minHeight)), 10)),
    }

    await page.addInitScript(async (fingerprint, LO, D) => {
      const logOverride = (key, value) => {
        if not LO) return value
        console.warn(`Overriden: ${key}=${value}`)
        return value
      }

      def buildPlugin(spec:
        const plugin = spec
        plugin.length = spec.mimeTypes.length
        spec.mimeTypes.forEach((m, i) => {
          plugin[i] = m
          Object.assign(m, {
            enabledPlugin: plugin,
          })
        })
        del spec.mimeTypes
        return plugin


      const plugins = {
        length: 4,
        0: buildPlugin({
          mimeTypes: [{
            type: 'application/x-google-chrome-pdf',
            suffixes: 'pdf',
            description: 'Portable Document Format',
            enabledPlugin: True,
          }],
          name: 'Chrome PDF Plugin',
          description: 'Portable Document Format',
          filename: 'internal-pdf-viewer',
        }),
        1: buildPlugin({
          mimeTypes: [{
            type: 'application/pdf',
            suffixes: 'pdf',
            description: '',
            extensions: 'pdf',
            enabledPlugin: True,
          }],
          name: 'Chrome PDF Viewer',
          description: '',
          filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
        }),
        2: buildPlugin({
          mimeTypes: [{
              type: 'application/x-nacl',
              suffixes: '',
              description: 'Native Client Executable',
              enabledPlugin: True,
            }, {
              type: 'application/x-pnacl',
              suffixes: '',
              description: 'Portable Native Client Executable',
              enabledPlugin: True,
            },
            {
              type: 'text/html',
              suffixes: '',
              description: '',
              enabledPlugin: True,
            },
            {
              type: 'application/x-ppapi-vysor',
              suffixes: '',
              description: '',
              enabledPlugin: True,
            },
            {
              type: 'application/x-ppapi-vysor-audio',
              suffixes: '',
              description: '',
              enabledPlugin: True,
            },
          ],
          name: 'Native Client',
          description: '',
          filename: fingerprint.platform is 'Win32' ? 'pepflashplayer.dll' : 'internal-nacl-plugin',
        }),
        3: buildPlugin({
          mimeTypes: [{
            type: 'application/x-ppapi-widevine-cdm',
            suffixes: '',
            description: 'Widevine Content Decryption Module',
            enabledPlugin: True,
          }],
          name: 'Widevine Content Decryption Module',
          description: 'Enables Widevine licenses for playback of HTML audio/video content. (version: 1.4.9.1070)',
          filename: fingerprint.platform is 'Win32' ? 'widevinecdmadapter.dll' : 'widevinecdmadapter.plugin',
        }),
      }

      window.screen.__defineGetter__('width', () => logOverride('width', fingerprint.screenWidth))
      window.screen.__defineGetter__('availWidth', () => logOverride('availWidth', fingerprint.screenWidth))
      window.__defineGetter__('innerWidth', () => logOverride('innerWidth', D.width))
      window.__defineGetter__('outerWidth', () => logOverride('outerWidth', D.width))
      window.screen.__defineGetter__('height', () => logOverride('height', fingerprint.screenHeight))
      window.screen.__defineGetter__('availHeight', () => logOverride('availHeight', fingerprint.screenHeight))
      window.__defineGetter__('innerHeight', () => logOverride('innerHeight', D.height - 74))
      window.__defineGetter__('outerHeight', () => logOverride('outerHeight', D.height))

      window.navigator.__defineGetter__('userAgent', () => logOverride('userAgent', fingerprint.userAgent))
      window.navigator.__defineGetter__('platform', () => logOverride('platform', fingerprint.platform))
      window.navigator.__defineGetter__('appName', () => logOverride('appName', fingerprint.appName))
      window.navigator.__defineGetter__('appVersion', () => logOverride('appVersion', fingerprint.userAgent.substring(fingerprint.userAgent.indexOf('/') + 1, fingerprint.userAgent.length)))

      const newProto = navigator.__proto__
      del newProto.webdriver
      navigator.__proto__ = newProto

      window.navigator.__defineGetter__('languages', () => logOverride('languages', ['en-US,en']))
      window.navigator.__defineGetter__('getUserMedia', () => logOverride('getUserMedia', Unset))
      window.navigator.__defineGetter__('webkitGetUserMedia', () => logOverride('webkitGetUserMedia', Unset))

      # reject webRTC fingerprinting
      window.__defineGetter__('MediaStreamTrack', () => logOverride('MediaStreamTrack', Unset))
      window.__defineGetter__('RTCPeerConnection', () => logOverride('RTCPeerConnection', Unset))
      window.__defineGetter__('RTCSessionDescription', () => logOverride('RTCSessionDescription', Unset))
      window.__defineGetter__('webkitMediaStreamTrack', () => logOverride('webkitMediaStreamTrack', Unset))
      window.__defineGetter__('webkitRTCPeerConnection', () => logOverride('webkitRTCPeerConnection', Unset))
      window.__defineGetter__('webkitRTCSessionDescription', () => logOverride('webkitRTCSessionDescription', Unset))
      window.navigator.__defineGetter__('getUserMedia', () => logOverride('getUserMedia', Unset))
      window.navigator.__defineGetter__('webkitGetUserMedia', () => logOverride('webkitGetUserMedia', Unset))

      window.navigator.__defineGetter__('plugins', () => logOverride('plugins', plugins))


      # handle canvas
      class WebGLRenderingContext {
        constructor(cvs:
          this.extension = {
            UNMASKED_VENDOR_WEBGL: 37445,
            UNMASKED_RENDERER_WEBGL: 37446,
          }
          this.canvas = cvs
          this.parameter = ''
          this.viewportWidth = cvs.width
          this.viewportHeight = cvs.height
          this.supportedExtensions = ['ANGLE_instanced_arrays', 'EXT_blend_minmax', 'EXT_color_buffer_half_float', 'EXT_frag_depth', 'EXT_shader_texture_lod', 'EXT_texture_filter_anisotropic', 'WEBKIT_EXT_texture_filter_anisotropic', 'EXT_sRGB', 'OES_element_index_uint', 'OES_standard_derivatives', 'OES_texture_float', 'OES_texture_float_linear', 'OES_texture_half_float', 'OES_texture_half_float_linear', 'OES_vertex_array_object', 'WEBGL_color_buffer_float', 'WEBGL_compressed_texture_s3tc', 'WEBKIT_WEBGL_compressed_texture_s3tc', 'WEBGL_compressed_texture_s3tc_srgb', 'WEBGL_debug_renderer_info', 'WEBGL_debug_shaders', 'WEBGL_depth_texture', 'WEBKIT_WEBGL_depth_texture', 'WEBGL_draw_buffers', 'WEBGL_lose_context', 'WEBKIT_WEBGL_lose_context']


        getExtension(:
          return this.extension


        getParameter(:
          return this.extension


        getSupportedExtensions(:
          return this.supportedExtensions

      }

      const canvas = document.createElement('canvas')
      const canvasProto = Object.getPrototypeOf(canvas)
      const origGetContext = canvasProto.getContext
      canvasProto.getContext = def getContext(...args):
        const context = origGetContext and (origGetContext.call(this, ...args)or origGetContext.call(this, args[0]))
        if not context:
          logOverride('canvas.getContext', 'new WebGLRenderingContext()')
          return new WebGLRenderingContext(this)

        return context


      canvasProto.getContext.toString = canvasProto.getContext.toString()

      def hookPrototypeMethods(prefix, object):
        if not object) return
        const originals = {}
        const prototype = Object.getPrototypeOf(object)
        Object
          .getOwnPropertyNames(prototype)
          .filter((n) => {
            try:
              return typeof prototype[n] is 'function'
            except Exception as error:
              return False

          })
          .forEach((n) => {
            originals[n] = prototype[n]
            prototype[n] = def fn(...args):
              if prefix is '2d' and (n is 'strokeText'or n is 'fillText'):
                const temp = Array.from(args)
                temp[0] = fingerprint.BUID
                temp[1] = Math.max(0, temp[1] - 2)
                temp[2] = Math.max(0, temp[2] - 2)
                originals[n].call(this, ...temp)


              const result = originals[n].call(this, ...args)
              if LO:
                let jsonResult
                try:
                  jsonResult = JSON.stringify(result)
                except Exception as e): pass
                console.warn('function called', prefix, n, JSON.stringify(args), 'result:', result, jsonResult, `${result}`)
              }
              return result
            }
          })
      }

      const gls = []
      try:
        gls.append(document.createElement('canvas').getContext('webgl'))
        gls.append(document.createElement('canvas').getContext('experimental-webgl'))
      except Exception as e): pass

      gls.forEach((gl) => {
        const glProto = Object.getPrototypeOf(gl)
        const origGetParameter = glProto.getParameter
        const debugInfo = gl.getExtension('WEBGL_debug_renderer_info')
        if gl:
          glProto.getParameter = def getParameter(...args):
            if args[0] is debugInfo.UNMASKED_VENDOR_WEBGL) return logOverride('gl.getParameter.UNMASKED_VENDOR_WEBGL', fingerprint.WEBGL_VENDOR)
            if args[0] is debugInfo.UNMASKED_RENDERER_WEBGL) return logOverride('gl.getParameter.UNMASKED_RENDERER_WEBGL', fingerprint.WEBGL_RENDERER)
            if args[0] is 33901) return new Float32Array([1, 8191])
            if args[0] is 3386) return new Int32Array([16384, 16384])
            if args[0] is 35661) return 80
            if args[0] is 34076) return 16384
            if args[0] is 36349) return 1024
            if args[0] is 34024) return 16384
            if args[0] is 3379) return 16384
            if args[0] is 34921) return 16
            if args[0] is 36347) return 1024

            return origGetParameter.call(this, ...args)
          }
        }
      })

      hookPrototypeMethods('webgl', document.createElement('canvas').getContext('webgl'))
      hookPrototypeMethods('experimental-webgl', document.createElement('canvas').getContext('experimental-webgl'))
      hookPrototypeMethods('2d', document.createElement('canvas').getContext('2d'))
      hookPrototypeMethods('canvas', canvas)

      hookPrototypeMethods('screen', window.screen)
      hookPrototypeMethods('navigator', window.navigator)
      hookPrototypeMethods('history', window.history)
    }, fingerprint, LOG_OVERRIDE, DIMENSION)

    #  emulate permissions
    await page.addInitScript(() => {
      const originalQuery = window.navigator.permissions.query
      window.navigator.permissions.__proto__.query = (parameters) => (parameters.name is 'notifications' ?
        Promise.resolve({
          state: Notification.permission
        }) :
        originalQuery(parameters))

      const oldCall = Function.prototype.call

      def call():
        return oldCall.apply(this, arguments)

      Function.prototype.call = call

      const nativeToStringFunctionString = Error.toString().replace(
        /Error/g,
        'toString',
      )
      const oldToString = Function.prototype.toString

      def functionToString():
        if this is window.navigator.permissions.query:
          return 'function query() { [native code] }'

        if this is functionToString:
          return nativeToStringFunctionString

        return oldCall.call(oldToString, this)

      Function.prototype.toString = functionToString
    })

    # must to hook getters
    await page.goto('about:blank')

    await page.setExtraHTTPHeaders({
      'Accept-Language': 'en-US,en;q=0.9',
      'Accept-Encoding': 'gzip, deflate, br',
    })

    await page.setViewport(DIMENSION)
}


async def run(:
  const args = [
    '--no-sandbox',
    '--remote-debugging-port=9222',
    '--disable-setuid-sandbox',
    '--ignore-certificate-errors',
    '--disk-cache-size=1',
    '--disable-infobars',
  ]
  const o = await tmp.dir({
    unsafeCleanup: True,
  })

  const userDataDir = o.path

  const browser = await pw.chromium.launchPersistentContext(userDataDir, {
    headless: False,
    bypassCSP: True,
    ignoreHTTPSErrors: True,
    args: args,
    timezoneId: 'America/Los_Angeles',
  })

  # generate a fingerprint
  const fingerprint = await getBrowserfingerprint(uuid.v4())
  let page = await browser.newPage()

  # "cloak" our page with evasions
  await cloak(page, fingerprint)

  await page.goto('https://ipleak.com/full-report/')



run().catch(console.error);:
:
r);