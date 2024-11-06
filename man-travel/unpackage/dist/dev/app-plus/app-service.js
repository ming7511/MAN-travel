if (typeof Promise !== "undefined" && !Promise.prototype.finally) {
  Promise.prototype.finally = function(callback) {
    const promise = this.constructor;
    return this.then(
      (value) => promise.resolve(callback()).then(() => value),
      (reason) => promise.resolve(callback()).then(() => {
        throw reason;
      })
    );
  };
}
;
if (typeof uni !== "undefined" && uni && uni.requireGlobal) {
  const global = uni.requireGlobal();
  ArrayBuffer = global.ArrayBuffer;
  Int8Array = global.Int8Array;
  Uint8Array = global.Uint8Array;
  Uint8ClampedArray = global.Uint8ClampedArray;
  Int16Array = global.Int16Array;
  Uint16Array = global.Uint16Array;
  Int32Array = global.Int32Array;
  Uint32Array = global.Uint32Array;
  Float32Array = global.Float32Array;
  Float64Array = global.Float64Array;
  BigInt64Array = global.BigInt64Array;
  BigUint64Array = global.BigUint64Array;
}
;
if (uni.restoreGlobal) {
  uni.restoreGlobal(Vue, weex, plus, setTimeout, clearTimeout, setInterval, clearInterval);
}
(function(vue) {
  "use strict";
  const _imports_0 = "/static/logo.png";
  const _imports_1 = "/static/logo3.png";
  const _export_sfc = (sfc, props) => {
    const target = sfc.__vccOpts || sfc;
    for (const [key, val] of props) {
      target[key] = val;
    }
    return target;
  };
  const _sfc_main$3 = {
    name: "IndexPage",
    mounted() {
      setTimeout(() => {
        uni.navigateTo({
          url: "/pages/login/login"
        });
      }, 3e3);
    }
  };
  function _sfc_render$2(_ctx, _cache, $props, $setup, $data, $options) {
    return vue.openBlock(), vue.createElementBlock("view", { class: "container" }, [
      vue.createCommentVNode(" 中间 logo 图片 "),
      vue.createElementVNode("view", { class: "middle-logo" }, [
        vue.createElementVNode("image", {
          src: _imports_0,
          alt: "Middle Logo",
          class: "logo-image-large"
        })
      ]),
      vue.createCommentVNode(" 底部图片 "),
      vue.createElementVNode("view", { class: "bottom-image" }, [
        vue.createElementVNode("image", {
          src: _imports_1,
          alt: "Bottom Logo",
          class: "logo-image"
        })
      ])
    ]);
  }
  const PagesWelcomeWelcome = /* @__PURE__ */ _export_sfc(_sfc_main$3, [["render", _sfc_render$2], ["__scopeId", "data-v-085f0530"], ["__file", "D:/Users/ROG/Documents/HBuilderProjects/man-travel/pages/welcome/welcome.vue"]]);
  function formatAppLog(type, filename, ...args) {
    if (uni.__log__) {
      uni.__log__(type, filename, ...args);
    } else {
      console[type].apply(console, [...args, filename]);
    }
  }
  const _sfc_main$2 = {
    name: "LoginPage",
    data() {
      return {
        phoneNumber: "",
        verificationCode: ""
      };
    },
    methods: {
      getVerificationCode() {
        formatAppLog("log", "at pages/login/login.vue:40", "获取验证码");
      },
      login() {
        if (this.phoneNumber && this.verificationCode) {
          uni.redirectTo({
            url: "/pages/index/index"
          });
        } else {
          uni.showToast({
            title: "请输入手机号和验证码",
            icon: "none"
          });
        }
      }
    }
  };
  function _sfc_render$1(_ctx, _cache, $props, $setup, $data, $options) {
    return vue.openBlock(), vue.createElementBlock("view", { class: "container" }, [
      vue.createCommentVNode(" Logo 图片 "),
      vue.createElementVNode("view", { class: "logo-section" }, [
        vue.createElementVNode("image", {
          src: _imports_0,
          alt: "Logo",
          class: "logo-image"
        }),
        vue.createElementVNode("image", {
          src: _imports_1,
          alt: "man游 Logo",
          class: "text-logo-image"
        })
      ]),
      vue.createCommentVNode(" 输入框区域 "),
      vue.createElementVNode("view", { class: "input-section" }, [
        vue.createCommentVNode(" 手机号码输入框 "),
        vue.createElementVNode("view", { class: "input-wrapper" }, [
          vue.withDirectives(vue.createElementVNode(
            "input",
            {
              type: "text",
              placeholder: "请输入手机号",
              class: "input",
              "onUpdate:modelValue": _cache[0] || (_cache[0] = ($event) => $data.phoneNumber = $event)
            },
            null,
            512
            /* NEED_PATCH */
          ), [
            [vue.vModelText, $data.phoneNumber]
          ])
        ]),
        vue.createCommentVNode(" 验证码输入框和按钮 "),
        vue.createElementVNode("view", { class: "verification-input-wrapper" }, [
          vue.withDirectives(vue.createElementVNode(
            "input",
            {
              type: "text",
              placeholder: "请输入验证码",
              class: "input",
              "onUpdate:modelValue": _cache[1] || (_cache[1] = ($event) => $data.verificationCode = $event)
            },
            null,
            512
            /* NEED_PATCH */
          ), [
            [vue.vModelText, $data.verificationCode]
          ]),
          vue.createElementVNode("button", {
            class: "verification-button",
            onClick: _cache[2] || (_cache[2] = (...args) => $options.getVerificationCode && $options.getVerificationCode(...args))
          }, "获取验证码")
        ])
      ]),
      vue.createCommentVNode(" 登录按钮 "),
      vue.createElementVNode("view", { class: "login-button-wrapper" }, [
        vue.createElementVNode("button", {
          class: "login-button",
          onClick: _cache[3] || (_cache[3] = (...args) => $options.login && $options.login(...args))
        }, "登录")
      ])
    ]);
  }
  const PagesLoginLogin = /* @__PURE__ */ _export_sfc(_sfc_main$2, [["render", _sfc_render$1], ["__scopeId", "data-v-e4e4508d"], ["__file", "D:/Users/ROG/Documents/HBuilderProjects/man-travel/pages/login/login.vue"]]);
  const _sfc_main$1 = {
    name: "IndexPage",
    mounted() {
      setTimeout(() => {
        uni.navigateTo({
          url: "/pages/login/login"
        });
      }, 1e5);
    }
  };
  function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
    return vue.openBlock(), vue.createElementBlock("view", { class: "container" }, [
      vue.createCommentVNode(" 中间 logo 图片 "),
      vue.createElementVNode("view", { class: "middle-logo" }, [
        vue.createElementVNode("image", {
          src: _imports_0,
          alt: "Middle Logo",
          class: "logo-image-large"
        })
      ]),
      vue.createCommentVNode(" 底部图片 "),
      vue.createElementVNode("view", { class: "bottom-image" }, [
        vue.createElementVNode("image", {
          src: _imports_1,
          alt: "Bottom Logo",
          class: "logo-image"
        })
      ])
    ]);
  }
  const PagesIndexIndex = /* @__PURE__ */ _export_sfc(_sfc_main$1, [["render", _sfc_render], ["__scopeId", "data-v-1cf27b2a"], ["__file", "D:/Users/ROG/Documents/HBuilderProjects/man-travel/pages/index/index.vue"]]);
  __definePage("pages/welcome/welcome", PagesWelcomeWelcome);
  __definePage("pages/login/login", PagesLoginLogin);
  __definePage("pages/index/index", PagesIndexIndex);
  const _sfc_main = {
    onLaunch: function() {
      formatAppLog("log", "at App.vue:4", "App Launch");
    },
    onShow: function() {
      formatAppLog("log", "at App.vue:7", "App Show");
    },
    onHide: function() {
      formatAppLog("log", "at App.vue:10", "App Hide");
    }
  };
  const App = /* @__PURE__ */ _export_sfc(_sfc_main, [["__file", "D:/Users/ROG/Documents/HBuilderProjects/man-travel/App.vue"]]);
  function createApp() {
    const app = vue.createVueApp(App);
    return {
      app
    };
  }
  const { app: __app__, Vuex: __Vuex__, Pinia: __Pinia__ } = createApp();
  uni.Vuex = __Vuex__;
  uni.Pinia = __Pinia__;
  __app__.provide("__globalStyles", __uniConfig.styles);
  __app__._component.mpType = "app";
  __app__._component.render = () => {
  };
  __app__.mount("#app");
})(Vue);
