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
  const _imports_0$1 = "/static/logo.png";
  const _export_sfc = (sfc, props) => {
    const target = sfc.__vccOpts || sfc;
    for (const [key, val] of props) {
      target[key] = val;
    }
    return target;
  };
  const _sfc_main$8 = {
    __name: "welcome",
    setup(__props, { expose: __expose }) {
      __expose();
      const { proxy } = vue.getCurrentInstance();
      const goToEditPage = () => {
        proxy.uni.navigateTo({
          url: "/pages/edit-profile/edit-profile"
          // 指定目标页面的路径
        });
      };
      const goToFeedback = () => {
        proxy.uni.navigateTo({
          url: "/pages/feedback/feedback"
        });
      };
      const goToAboutUs = () => {
        proxy.uni.navigateTo({
          url: "/pages/about-us/about-us"
        });
      };
      const __returned__ = { proxy, goToEditPage, goToFeedback, goToAboutUs, getCurrentInstance: vue.getCurrentInstance };
      Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
      return __returned__;
    }
  };
  function _sfc_render$7(_ctx, _cache, $props, $setup, $data, $options) {
    return vue.openBlock(), vue.createElementBlock("div", { class: "profile-page" }, [
      vue.createCommentVNode(" 顶部个人信息 "),
      vue.createElementVNode("div", { class: "profile-header" }, [
        vue.createElementVNode("img", {
          class: "avatar",
          src: _imports_0$1,
          alt: "avatar"
        }),
        vue.createElementVNode("div", { class: "username" }, "一个真正的man"),
        vue.createCommentVNode(" 右上角编辑按钮，改为灰色字体的可点击文本 "),
        vue.createElementVNode("div", {
          class: "edit-link",
          onClick: $setup.goToEditPage
        }, "编辑")
      ]),
      vue.createCommentVNode(" 旅行数据统计 "),
      vue.createElementVNode("div", { class: "travel-stats" }, [
        vue.createElementVNode("div", { class: "stat-item" }, [
          vue.createElementVNode("div", { class: "stat-value" }, "211"),
          vue.createElementVNode("div", { class: "stat-label" }, "旅行次数")
        ]),
        vue.createElementVNode("div", { class: "stat-item" }, [
          vue.createElementVNode("div", { class: "stat-value" }, "19"),
          vue.createElementVNode("div", { class: "stat-label" }, "旅行天数")
        ]),
        vue.createElementVNode("div", { class: "stat-item" }, [
          vue.createElementVNode("div", { class: "stat-value" }, "630km"),
          vue.createElementVNode("div", { class: "stat-label" }, "总里程")
        ])
      ]),
      vue.createCommentVNode(" 功能选项 "),
      vue.createElementVNode("div", { class: "options-list" }, [
        vue.createElementVNode("div", {
          class: "option-item",
          onClick: $setup.goToFeedback
        }, [
          vue.createElementVNode("i", { class: "icon feedback-icon" }, "💬"),
          vue.createElementVNode("span", null, "建议反馈"),
          vue.createElementVNode("span", { class: "arrow-symbol" }, ">")
        ]),
        vue.createElementVNode("div", {
          class: "option-item",
          onClick: $setup.goToAboutUs
        }, [
          vue.createElementVNode("i", { class: "icon about-icon" }, "ℹ️"),
          vue.createElementVNode("span", null, "关于我们"),
          vue.createElementVNode("span", { class: "arrow-symbol" }, ">")
        ])
      ])
    ]);
  }
  const PagesWelcomeWelcome = /* @__PURE__ */ _export_sfc(_sfc_main$8, [["render", _sfc_render$7], ["__scopeId", "data-v-085f0530"], ["__file", "D:/Users/ROG/Documents/HBuilderProjects/man-travel/pages/welcome/welcome.vue"]]);
  function formatAppLog(type, filename, ...args) {
    if (uni.__log__) {
      uni.__log__(type, filename, ...args);
    } else {
      console[type].apply(console, [...args, filename]);
    }
  }
  const _imports_1 = "/static/logo3.png";
  const _sfc_main$7 = {
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
  function _sfc_render$6(_ctx, _cache, $props, $setup, $data, $options) {
    return vue.openBlock(), vue.createElementBlock("view", { class: "container" }, [
      vue.createCommentVNode(" Logo 图片 "),
      vue.createElementVNode("view", { class: "logo-section" }, [
        vue.createElementVNode("image", {
          src: _imports_0$1,
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
  const PagesLoginLogin = /* @__PURE__ */ _export_sfc(_sfc_main$7, [["render", _sfc_render$6], ["__scopeId", "data-v-e4e4508d"], ["__file", "D:/Users/ROG/Documents/HBuilderProjects/man-travel/pages/login/login.vue"]]);
  const _sfc_main$6 = {
    name: "IndexPage",
    mounted() {
      setTimeout(() => {
        uni.navigateTo({
          url: "/pages/login/login"
        });
      }, 1e5);
    }
  };
  function _sfc_render$5(_ctx, _cache, $props, $setup, $data, $options) {
    return vue.openBlock(), vue.createElementBlock("view", { class: "container" }, [
      vue.createCommentVNode(" 中间 logo 图片 "),
      vue.createElementVNode("view", { class: "middle-logo" }, [
        vue.createElementVNode("image", {
          src: _imports_0$1,
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
  const PagesIndexIndex = /* @__PURE__ */ _export_sfc(_sfc_main$6, [["render", _sfc_render$5], ["__scopeId", "data-v-1cf27b2a"], ["__file", "D:/Users/ROG/Documents/HBuilderProjects/man-travel/pages/index/index.vue"]]);
  const _sfc_main$5 = {
    __name: "about-us",
    setup(__props, { expose: __expose }) {
      __expose();
      const goBack = () => {
        uni.navigateBack({
          delta: 1
        });
      };
      const goToFunctionIntroduction = () => {
        uni.navigateTo({
          url: "/pages/function-introduction/function-introduction"
        });
      };
      const goToSuggestion = () => {
        uni.navigateTo({
          url: "/pages/suggestion/suggestion"
          // 更新跳转路径到 suggestion 页面
        });
      };
      const checkForUpdate = () => {
        uni.showToast({
          title: "当前已是最新版本",
          icon: "none"
        });
      };
      const __returned__ = { goBack, goToFunctionIntroduction, goToSuggestion, checkForUpdate };
      Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
      return __returned__;
    }
  };
  function _sfc_render$4(_ctx, _cache, $props, $setup, $data, $options) {
    return vue.openBlock(), vue.createElementBlock("div", { class: "about-page" }, [
      vue.createCommentVNode(" 顶部返回按钮 "),
      vue.createElementVNode("div", { class: "header" }, [
        vue.createElementVNode("div", {
          class: "back-button",
          onClick: $setup.goBack
        }, "＜ 返回")
      ]),
      vue.createCommentVNode(" 应用信息 "),
      vue.createElementVNode("div", { class: "app-info" }, [
        vue.createElementVNode("image", {
          src: _imports_0$1,
          alt: "Bottom Logo",
          class: "logo-image"
        }),
        vue.createElementVNode("div", { class: "app-name" }, "Man游"),
        vue.createElementVNode("div", { class: "app-version" }, "Version 1.0.0")
      ]),
      vue.createCommentVNode(" 功能选项列表 "),
      vue.createElementVNode("div", { class: "options-list" }, [
        vue.createElementVNode("div", {
          class: "option-item",
          onClick: $setup.goToFunctionIntroduction
        }, [
          vue.createElementVNode("span", null, "功能介绍"),
          vue.createElementVNode("span", { class: "arrow-symbol" }, ">")
        ]),
        vue.createElementVNode("div", {
          class: "option-item",
          onClick: $setup.goToSuggestion
        }, [
          vue.createElementVNode("span", null, "投诉"),
          vue.createElementVNode("span", { class: "arrow-symbol" }, ">")
        ]),
        vue.createElementVNode("div", {
          class: "option-item",
          onClick: $setup.checkForUpdate
        }, [
          vue.createElementVNode("span", null, "检查新版本"),
          vue.createElementVNode("span", { class: "arrow-symbol" }, ">")
        ])
      ]),
      vue.createCommentVNode(" 版权信息 "),
      vue.createElementVNode("div", { class: "footer" }, [
        vue.createElementVNode("div", null, "iman团队 版权所有"),
        vue.createElementVNode("div", null, "All Rights Reserved")
      ])
    ]);
  }
  const PagesAboutUsAboutUs = /* @__PURE__ */ _export_sfc(_sfc_main$5, [["render", _sfc_render$4], ["__scopeId", "data-v-4de12c27"], ["__file", "D:/Users/ROG/Documents/HBuilderProjects/man-travel/pages/about-us/about-us.vue"]]);
  const _sfc_main$4 = {
    __name: "user",
    setup(__props, { expose: __expose }) {
      __expose();
      const goToEditPage = () => {
        uni.navigateTo({
          url: "/pages/edit-profile/edit-profile"
          // 指定目标页面的路径
        });
      };
      const goToFeedback = () => {
        uni.navigateTo({
          url: "/pages/suggestion/suggestion"
        });
      };
      const goToAboutUs = () => {
        uni.navigateTo({
          url: "/pages/about-us/about-us"
        });
      };
      const __returned__ = { goToEditPage, goToFeedback, goToAboutUs };
      Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
      return __returned__;
    }
  };
  function _sfc_render$3(_ctx, _cache, $props, $setup, $data, $options) {
    return vue.openBlock(), vue.createElementBlock("div", { class: "profile-page" }, [
      vue.createCommentVNode(" 顶部个人信息 "),
      vue.createElementVNode("div", { class: "profile-header" }, [
        vue.createElementVNode("image", {
          class: "avatar",
          src: _imports_0$1,
          alt: "avatar"
        }),
        vue.createElementVNode("div", { class: "username" }, "一个真正的man"),
        vue.createCommentVNode(" 右上角编辑按钮，改为灰色字体的可点击文本 "),
        vue.createElementVNode("div", {
          class: "edit-link",
          onClick: $setup.goToEditPage
        }, "编辑")
      ]),
      vue.createCommentVNode(" 旅行数据统计 "),
      vue.createElementVNode("div", { class: "travel-stats" }, [
        vue.createElementVNode("div", { class: "stat-item" }, [
          vue.createElementVNode("div", { class: "stat-value" }, "211"),
          vue.createElementVNode("div", { class: "stat-label" }, "旅行次数")
        ]),
        vue.createElementVNode("div", { class: "stat-item" }, [
          vue.createElementVNode("div", { class: "stat-value" }, "19"),
          vue.createElementVNode("div", { class: "stat-label" }, "旅行天数")
        ]),
        vue.createElementVNode("div", { class: "stat-item" }, [
          vue.createElementVNode("div", { class: "stat-value" }, "630km"),
          vue.createElementVNode("div", { class: "stat-label" }, "总里程")
        ])
      ]),
      vue.createCommentVNode(" 功能选项 "),
      vue.createElementVNode("div", { class: "options-list" }, [
        vue.createElementVNode("div", {
          class: "option-item",
          onClick: $setup.goToFeedback
        }, [
          vue.createElementVNode("i", { class: "icon feedback-icon" }, "💬"),
          vue.createElementVNode("span", null, "建议反馈"),
          vue.createElementVNode("span", { class: "arrow-symbol" }, ">")
        ]),
        vue.createElementVNode("div", {
          class: "option-item",
          onClick: $setup.goToAboutUs
        }, [
          vue.createElementVNode("i", { class: "icon about-icon" }, "ℹ️"),
          vue.createElementVNode("span", null, "关于我们"),
          vue.createElementVNode("span", { class: "arrow-symbol" }, ">")
        ])
      ])
    ]);
  }
  const PagesUserUser = /* @__PURE__ */ _export_sfc(_sfc_main$4, [["render", _sfc_render$3], ["__scopeId", "data-v-0f7520f0"], ["__file", "D:/Users/ROG/Documents/HBuilderProjects/man-travel/pages/user/user.vue"]]);
  const _sfc_main$3 = {
    __name: "suggestion",
    setup(__props, { expose: __expose }) {
      __expose();
      const feedbackText = vue.ref("");
      const goBack = () => {
        uni.navigateBack({
          delta: 1
        });
      };
      const chooseImage = () => {
        uni.chooseImage({
          count: 1,
          success: (res) => {
            uni.showToast({
              title: "图片已选择",
              icon: "success"
            });
            formatAppLog("log", "at pages/suggestion/suggestion.vue:56", "选择的图片路径:", res.tempFilePaths);
          },
          fail: (err) => {
            formatAppLog("error", "at pages/suggestion/suggestion.vue:59", "图片选择失败:", err);
          }
        });
      };
      const submitFeedback = () => {
        if (!feedbackText.value.trim()) {
          uni.showToast({
            title: "请填写反馈内容",
            icon: "none"
          });
          return;
        }
        uni.showToast({
          title: "反馈已提交",
          icon: "success"
        });
        formatAppLog("log", "at pages/suggestion/suggestion.vue:78", "反馈内容:", feedbackText.value);
      };
      const __returned__ = { feedbackText, goBack, chooseImage, submitFeedback, ref: vue.ref };
      Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
      return __returned__;
    }
  };
  function _sfc_render$2(_ctx, _cache, $props, $setup, $data, $options) {
    return vue.openBlock(), vue.createElementBlock("div", { class: "feedback-page" }, [
      vue.createCommentVNode(" 顶部返回按钮和标题 "),
      vue.createElementVNode("div", { class: "header" }, [
        vue.createElementVNode("div", {
          class: "back-button",
          onClick: $setup.goBack
        }, "＜ 返回"),
        vue.createElementVNode("div", { class: "title" }, "反馈建议")
      ]),
      vue.createCommentVNode(" 描述输入框 "),
      vue.createElementVNode("div", { class: "description-box" }, [
        vue.withDirectives(vue.createElementVNode(
          "textarea",
          {
            "onUpdate:modelValue": _cache[0] || (_cache[0] = ($event) => $setup.feedbackText = $event),
            placeholder: "描述问题的详细情况，有助于我们快速帮您解决（必填）",
            rows: "5",
            class: "feedback-textarea"
          },
          null,
          512
          /* NEED_PATCH */
        ), [
          [vue.vModelText, $setup.feedbackText]
        ])
      ]),
      vue.createCommentVNode(" 添加图片按钮 "),
      vue.createElementVNode("div", { class: "image-upload" }, [
        vue.createElementVNode("div", {
          class: "upload-box",
          onClick: $setup.chooseImage
        }, [
          vue.createElementVNode("div", { class: "add-icon" }, "+"),
          vue.createElementVNode("div", { class: "upload-text" }, "添加图")
        ])
      ]),
      vue.createCommentVNode(" 提交按钮 "),
      vue.createElementVNode("div", {
        class: "submit-button",
        onClick: $setup.submitFeedback
      }, " 提交 ")
    ]);
  }
  const PagesSuggestionSuggestion = /* @__PURE__ */ _export_sfc(_sfc_main$3, [["render", _sfc_render$2], ["__scopeId", "data-v-ab9b9b5a"], ["__file", "D:/Users/ROG/Documents/HBuilderProjects/man-travel/pages/suggestion/suggestion.vue"]]);
  const _sfc_main$2 = {
    __name: "function-introduction",
    setup(__props, { expose: __expose }) {
      __expose();
      const goBack = () => {
        uni.navigateBack({
          delta: 1
        });
      };
      const __returned__ = { goBack };
      Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
      return __returned__;
    }
  };
  function _sfc_render$1(_ctx, _cache, $props, $setup, $data, $options) {
    return vue.openBlock(), vue.createElementBlock("div", { class: "intro-page" }, [
      vue.createCommentVNode(" 顶部返回按钮 "),
      vue.createElementVNode("div", { class: "header" }, [
        vue.createElementVNode("div", {
          class: "back-button",
          onClick: $setup.goBack
        }, "＜ 返回")
      ]),
      vue.createCommentVNode(" 应用名称和介绍信息 "),
      vue.createElementVNode("div", { class: "intro-content" }, [
        vue.createElementVNode("div", { class: "app-name" }, "Man游"),
        vue.createElementVNode("div", { class: "app-description" }, " Man游在旅游规划与行程管理的生态系统中，是一个重要的信息处理中枢。它不仅能够接收用户输入的旅游相关推文或链接，还能够智能地解析这些信息，并自动生成详细的旅游计划。这种自动化处理能力极大地提高了用户的旅游规划效率，使用户能够更加轻松、快捷地规划出符合自己需求的旅游行程。 ")
      ])
    ]);
  }
  const PagesFunctionIntroductionFunctionIntroduction = /* @__PURE__ */ _export_sfc(_sfc_main$2, [["render", _sfc_render$1], ["__scopeId", "data-v-66966164"], ["__file", "D:/Users/ROG/Documents/HBuilderProjects/man-travel/pages/function-introduction/function-introduction.vue"]]);
  const _imports_0 = "/static/avatar.png";
  const _sfc_main$1 = {
    __name: "edit-profile",
    setup(__props, { expose: __expose }) {
      __expose();
      const goBack = () => {
        uni.navigateBack({
          delta: 1
        });
      };
      const editAvatar = () => {
        uni.chooseImage({
          count: 1,
          success: (res) => {
            uni.showToast({
              title: "头像已选择",
              icon: "success"
            });
            formatAppLog("log", "at pages/edit-profile/edit-profile.vue:67", "选择的头像路径:", res.tempFilePaths);
          },
          fail: (err) => {
            formatAppLog("error", "at pages/edit-profile/edit-profile.vue:70", "头像选择失败:", err);
          }
        });
      };
      const editNickname = () => {
        uni.showModal({
          title: "编辑昵称",
          editable: true,
          placeholderText: "请输入新的昵称",
          success: (res) => {
            if (res.confirm && res.content) {
              uni.showToast({
                title: `昵称已修改为 ${res.content}`,
                icon: "success"
              });
            }
          }
        });
      };
      const editRealName = () => {
        uni.showModal({
          title: "编辑真实姓名",
          editable: true,
          placeholderText: "请输入真实姓名",
          success: (res) => {
            if (res.confirm && res.content) {
              uni.showToast({
                title: `真实姓名已修改为 ${res.content}`,
                icon: "success"
              });
            }
          }
        });
      };
      const editGender = () => {
        uni.showActionSheet({
          itemList: ["男", "女"],
          success: (res) => {
            const gender = res.tapIndex === 0 ? "男" : "女";
            uni.showToast({
              title: `性别已修改为 ${gender}`,
              icon: "success"
            });
          }
        });
      };
      const submitChanges = () => {
        uni.showToast({
          title: "信息已保存",
          icon: "success"
        });
      };
      const __returned__ = { goBack, editAvatar, editNickname, editRealName, editGender, submitChanges, ref: vue.ref };
      Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
      return __returned__;
    }
  };
  function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
    return vue.openBlock(), vue.createElementBlock("div", { class: "edit-profile-page" }, [
      vue.createCommentVNode(" 顶部返回按钮和标题 "),
      vue.createElementVNode("div", { class: "header" }, [
        vue.createElementVNode("div", {
          class: "back-button",
          onClick: $setup.goBack
        }, "＜ 返回"),
        vue.createElementVNode("div", { class: "title" }, "个人信息")
      ]),
      vue.createCommentVNode(" 头像编辑 "),
      vue.createElementVNode("div", {
        class: "profile-item avatar-item",
        onClick: $setup.editAvatar
      }, [
        vue.createElementVNode("span", { class: "label" }, "头像"),
        vue.createElementVNode("image", {
          src: _imports_0,
          alt: "头像",
          class: "avatar-image"
        }),
        vue.createElementVNode("span", { class: "arrow" }, ">")
      ]),
      vue.createCommentVNode(" 信息编辑列表 "),
      vue.createElementVNode("div", {
        class: "profile-item",
        onClick: $setup.editNickname
      }, [
        vue.createElementVNode("span", { class: "label" }, "昵称"),
        vue.createElementVNode("span", { class: "value" }, "一个真正的man"),
        vue.createElementVNode("span", { class: "arrow" }, ">")
      ]),
      vue.createElementVNode("div", {
        class: "profile-item",
        onClick: $setup.editRealName
      }, [
        vue.createElementVNode("span", { class: "label" }, "真实姓名"),
        vue.createElementVNode("span", { class: "value" }, "小蓝龙"),
        vue.createElementVNode("span", { class: "arrow" }, ">")
      ]),
      vue.createElementVNode("div", {
        class: "profile-item",
        onClick: $setup.editGender
      }, [
        vue.createElementVNode("span", { class: "label" }, "性别"),
        vue.createElementVNode("span", { class: "value" }, "男"),
        vue.createElementVNode("span", { class: "arrow" }, ">")
      ]),
      vue.createElementVNode("div", { class: "profile-item" }, [
        vue.createElementVNode("span", { class: "label" }, "手机"),
        vue.createElementVNode("span", { class: "value" }, "189****9999")
      ]),
      vue.createElementVNode("div", { class: "profile-item" }, [
        vue.createElementVNode("span", { class: "label" }, "邮箱"),
        vue.createElementVNode("span", { class: "value" }, "189****9999@qq.com")
      ]),
      vue.createCommentVNode(" 提交按钮 "),
      vue.createElementVNode("div", {
        class: "submit-button",
        onClick: $setup.submitChanges
      }, " 保存 ")
    ]);
  }
  const PagesEditProfileEditProfile = /* @__PURE__ */ _export_sfc(_sfc_main$1, [["render", _sfc_render], ["__scopeId", "data-v-c0f45e44"], ["__file", "D:/Users/ROG/Documents/HBuilderProjects/man-travel/pages/edit-profile/edit-profile.vue"]]);
  __definePage("pages/welcome/welcome", PagesWelcomeWelcome);
  __definePage("pages/login/login", PagesLoginLogin);
  __definePage("pages/index/index", PagesIndexIndex);
  __definePage("pages/about-us/about-us", PagesAboutUsAboutUs);
  __definePage("pages/user/user", PagesUserUser);
  __definePage("pages/suggestion/suggestion", PagesSuggestionSuggestion);
  __definePage("pages/function-introduction/function-introduction", PagesFunctionIntroductionFunctionIntroduction);
  __definePage("pages/edit-profile/edit-profile", PagesEditProfileEditProfile);
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
