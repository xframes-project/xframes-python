#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/complex.h>
#include <pybind11/functional.h>
#include <pybind11/chrono.h>

#include <GLFW/glfw3.h>
#include <GLES3/gl3.h>

#include <functional>
#include <thread>
#include <cstdio>
#include <string>
#include <utility>
#include <vector>

#include <set>
#include <optional>
#include "imgui.h"
#include "implot.h"
#include "implot_internal.h"
#include <nlohmann/json.hpp>

#include "color_helpers.h"
#include "xframes.h"
#include "implot_renderer.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;
using json = nlohmann::json;

using OnInitCb = const std::function<void()>;
using OnTextChangedCb = const std::function<void(int, const std::string&)>;
using OnComboChangedCb = const std::function<void(int, int)>;
using OnNumericValueChangedCb = const std::function<void(int, float)>;
using OnBooleanValueChangedCb = const std::function<void(int, bool)>;
using OnMultipleNumericValuesChangedCb = const std::function<void(int, std::vector<float>)>;
using OnClickCb = const std::function<void(int)>;

template <typename T>
std::vector<T> JsonToVector(std::string& data) {
    auto parsedData = json::parse(data);
    std::vector<T> vec;
    for (auto& [key, item] : parsedData.items()) {
        vec.push_back(item.template get<T>());
    }
    return vec;
}

template <typename T>
std::set<T> JsonToSet(std::string& data) {
    auto parsedData = json::parse(data);
    std::set<T> set;
    for (auto& [key, item] : parsedData.items()) {
        set.insert(item.template get<T>());
    }
    return set;
}

json IntVectorToJson(const std::vector<int>& data) {
    auto jsonArray = json::array();
    for (auto& item : data) {
        jsonArray.push_back(item);
    }
    return jsonArray;
}

json IntSetToJson(const std::set<int>& data) {
    auto jsonArray = json::array();
    for (auto& item : data) {
        jsonArray.push_back(item);
    }
    return jsonArray;
}

class Runner {
    protected:
        XFrames* m_xframes{};
        ImGuiRenderer* m_renderer{};

        std::string m_rawFontDefs;
        std::string m_assetsBasePath;
        std::optional<std::string> m_rawStyleOverridesDefs;

        std::function<void()> m_onInit;
        std::function<void(int, const std::string&)> m_onTextChange;
        std::function<void(int, int)> m_onComboChange;
        std::function<void(int, float)> m_onNumericValueChange;
        std::function<void(int, bool)> m_onBooleanValueChange;
        std::function<void(int, std::vector<float>)> m_onMultipleNumericValuesChange;
        std::function<void(int)> m_onClick;

        static Runner* instance;

        Runner() {}
    public:
        static Runner* getInstance() {
            if (nullptr == instance) {
                instance = new Runner();
            }
            return instance;
        };

        ~Runner() {
            
        }

        static void OnInit() {
            auto pRunner = getInstance();

            pRunner->m_onInit();
        }

        static void OnTextChange(const int id, const std::string& value) {
            auto pRunner = getInstance();

        }

        static void OnComboChange(const int id, const int value) {
            auto pRunner = getInstance();

        }

        static void OnNumericValueChange(const int id, const float value) {
            auto pRunner = getInstance();

        }

        static void OnBooleanValueChange(const int id, const bool value) {
            auto pRunner = getInstance();

        }

        // todo: improve
        static void OnMultipleNumericValuesChange(const int id, const float* values, const int numValues) {
            auto pRunner = getInstance();


        }

        static void OnClick(int id) {
            auto pRunner = getInstance();

            pRunner->m_onClick(id);
        }

        void SetHandlers(
            OnInitCb& onInit,
            OnTextChangedCb& onTextChanged,
            OnComboChangedCb& onComboChanged,
            OnNumericValueChangedCb& onNumericValueChanged,
            OnBooleanValueChangedCb& onBooleanValueChanged,
            OnMultipleNumericValuesChangedCb& onMultipleNumericValuesChanged,
            OnClickCb& onClick
            ) {
                m_onInit = [onInit](){ onInit(); };
                m_onTextChange = [onTextChanged](int id, const std::string& value){ onTextChanged(id, value); };
                m_onComboChange = [onComboChanged](int id, int value){ onComboChanged(id, value); };
                m_onNumericValueChange = [onNumericValueChanged](int id, float value){ onNumericValueChanged(id, value); };
                m_onBooleanValueChange = [onBooleanValueChanged](int id, bool value){ onBooleanValueChanged(id, value); };
                m_onMultipleNumericValuesChange = [onMultipleNumericValuesChanged](int id, std::vector<float> values){ onMultipleNumericValuesChanged(id, values); };
                m_onClick = [onClick](int id){ onClick(id); };
        }

        void SetRawFontDefs(std::string rawFontDefs) {
            m_rawFontDefs = std::move(rawFontDefs);
        }

        void SetAssetsBasePath(std::string basePath) {
            m_assetsBasePath = basePath;
        }

        void SetRawStyleOverridesDefs(const std::string& rawStyleOverridesDefs) {
            m_rawStyleOverridesDefs.emplace(rawStyleOverridesDefs);
        }

        void init() {
            m_xframes = new XFrames("XFrames", m_rawStyleOverridesDefs);
            m_renderer = new ImPlotRenderer(
                m_xframes,
                "XFrames",
                "XFrames",
                m_rawFontDefs,
                m_assetsBasePath
            );
            // todo: do we need this?
            m_renderer->SetCurrentContext();

            m_xframes->SetEventHandlers(
                OnInit,
                OnTextChange,
                OnComboChange,
                OnNumericValueChange,
                OnMultipleNumericValuesChange,
                OnBooleanValueChange,
                OnClick
            );
        }

        void run() {
            m_renderer->Init();
        }

        void exit() const {
            // emscripten_cancel_main_loop();
            // emscripten_force_exit(0);
        }

        void resizeWindow(const int width, const int height) const {
            m_renderer->SetWindowSize(width, height);
        }

        void setElement(std::string& elementJsonAsString) const {
            m_xframes->QueueCreateElement(elementJsonAsString);
        }

        void patchElement(const int id, std::string& elementJsonAsString) const {
            m_xframes->QueuePatchElement(id, elementJsonAsString);
        }

        void elementInternalOp(const int id, std::string& elementJsonAsString) const {
            m_xframes->QueueElementInternalOp(id, elementJsonAsString);
        }

        void setChildren(const int id, const std::vector<int>& childrenIds) const {
            m_xframes->QueueSetChildren(id, childrenIds);
        }

        void appendChild(const int parentId, const int childId) const {
            m_xframes->QueueAppendChild(parentId, childId);
        }

        [[nodiscard]] std::vector<int> getChildren(const int id) const {
            return m_xframes->GetChildren(id);
        }

        [[nodiscard]] std::string getAvailableFonts() const {
            return m_renderer->GetAvailableFonts().dump();
        }

        void appendTextToClippedMultiLineTextRenderer(const int id, const std::string& data) const {
            m_xframes->AppendTextToClippedMultiLineTextRenderer(id, data);
        }

        [[nodiscard]] std::string getStyle() const {
            json style;

            style["alpha"] = m_xframes->m_appStyle.Alpha;
            style["disabledAlpha"] = m_xframes->m_appStyle.DisabledAlpha;
            style["windowPadding"] = { m_xframes->m_appStyle.WindowPadding.x, m_xframes->m_appStyle.WindowPadding.y };
            style["windowRounding"] = m_xframes->m_appStyle.WindowRounding;
            style["windowBorderSize"] = m_xframes->m_appStyle.WindowBorderSize;
            style["windowMinSize"] = { m_xframes->m_appStyle.WindowMinSize.x, m_xframes->m_appStyle.WindowMinSize.y };
            style["windowTitleAlign"] = { m_xframes->m_appStyle.WindowTitleAlign.x, m_xframes->m_appStyle.WindowTitleAlign.y };
            style["windowMenuButtonPosition"] = m_xframes->m_appStyle.WindowMenuButtonPosition;
            style["childRounding"] = m_xframes->m_appStyle.ChildRounding;
            style["childBorderSize"] = m_xframes->m_appStyle.ChildBorderSize;
            style["popupRounding"] = m_xframes->m_appStyle.PopupRounding;
            style["popupBorderSize"] = m_xframes->m_appStyle.PopupBorderSize;
            style["framePadding"] = { m_xframes->m_appStyle.FramePadding.x, m_xframes->m_appStyle.FramePadding.y };
            style["frameRounding"] = m_xframes->m_appStyle.FrameRounding;
            style["frameBorderSize"] = m_xframes->m_appStyle.FrameBorderSize;
            style["itemSpacing"] = { m_xframes->m_appStyle.ItemSpacing.x, m_xframes->m_appStyle.ItemSpacing.y };
            style["itemInnerSpacing"] = { m_xframes->m_appStyle.ItemInnerSpacing.x, m_xframes->m_appStyle.ItemInnerSpacing.y };
            style["cellPadding"] = { m_xframes->m_appStyle.CellPadding.x, m_xframes->m_appStyle.CellPadding.y };
            style["touchExtraPadding"] = { m_xframes->m_appStyle.TouchExtraPadding.x, m_xframes->m_appStyle.TouchExtraPadding.y };
            style["indentSpacing"] = m_xframes->m_appStyle.IndentSpacing;
            style["columnsMinSpacing"] = m_xframes->m_appStyle.ColumnsMinSpacing;
            style["scrollbarSize"] = m_xframes->m_appStyle.ScrollbarSize;
            style["scrollbarRounding"] = m_xframes->m_appStyle.ScrollbarRounding;
            style["grabMinSize"] = m_xframes->m_appStyle.GrabMinSize;
            style["grabRounding"] = m_xframes->m_appStyle.GrabRounding;
            style["logSliderDeadzone"] = m_xframes->m_appStyle.LogSliderDeadzone;
            style["tabRounding"] = m_xframes->m_appStyle.TabRounding;
            style["tabBorderSize"] = m_xframes->m_appStyle.TabBorderSize;
            style["tabMinWidthForCloseButton"] = m_xframes->m_appStyle.TabMinWidthForCloseButton;
            style["tabBarBorderSize"] = m_xframes->m_appStyle.TabBarBorderSize;
            style["tableAngledHeadersAngle"] = m_xframes->m_appStyle.TableAngledHeadersAngle;
            style["tableAngledHeadersTextAlign"] = { m_xframes->m_appStyle.TableAngledHeadersTextAlign.x, m_xframes->m_appStyle.TableAngledHeadersTextAlign.y };
            style["colorButtonPosition"] = m_xframes->m_appStyle.ColorButtonPosition;
            style["buttonTextAlign"] = { m_xframes->m_appStyle.ButtonTextAlign.x, m_xframes->m_appStyle.ButtonTextAlign.y };
            style["selectableTextAlign"] = { m_xframes->m_appStyle.SelectableTextAlign.x, m_xframes->m_appStyle.SelectableTextAlign.y };
            style["separatorTextPadding"] = { m_xframes->m_appStyle.SeparatorTextPadding.x, m_xframes->m_appStyle.SeparatorTextPadding.y };
            style["displayWindowPadding"] = { m_xframes->m_appStyle.DisplayWindowPadding.x, m_xframes->m_appStyle.DisplayWindowPadding.y };
            style["displaySafeAreaPadding"] = { m_xframes->m_appStyle.DisplaySafeAreaPadding.x, m_xframes->m_appStyle.DisplaySafeAreaPadding.y };
            style["mouseCursorScale"] = m_xframes->m_appStyle.MouseCursorScale;
            style["antiAliasedLines"] = m_xframes->m_appStyle.AntiAliasedLines;
            style["antiAliasedLinesUseTex"] = m_xframes->m_appStyle.AntiAliasedLinesUseTex;
            style["antiAliasedFill"] = m_xframes->m_appStyle.AntiAliasedFill;
            style["curveTessellationTol"] = m_xframes->m_appStyle.CurveTessellationTol;
            style["circleTessellationMaxError"] = m_xframes->m_appStyle.CircleTessellationMaxError;

            style["hoverStationaryDelay"] = m_xframes->m_appStyle.HoverStationaryDelay;
            style["hoverDelayShort"] = m_xframes->m_appStyle.HoverDelayShort;
            style["hoverDelayNormal"] = m_xframes->m_appStyle.HoverDelayNormal;

            style["hoverFlagsForTooltipMouse"] = m_xframes->m_appStyle.HoverFlagsForTooltipMouse;
            style["hoverFlagsForTooltipNav"] = m_xframes->m_appStyle.HoverFlagsForTooltipNav;

            style["colors"] = json::array();

            for (int i = 0; i < ImGuiCol_COUNT; i++) {
                auto maybeValue = IV4toJsonHEXATuple(m_xframes->m_appStyle.Colors[i]);

                if (maybeValue.has_value()) {
                    style["colors"].push_back(maybeValue.value());
                }
            }

            return style.dump();
        }

        void patchStyle(std::string& styleDef) const {
            m_xframes->PatchStyle(json::parse(styleDef));
        }

        void setDebug(const bool debug) const {
            m_xframes->SetDebug(debug);
        }

        void showDebugWindow() const {
            m_xframes->ShowDebugWindow();
        }
};

Runner* Runner::instance = nullptr;

void resizeWindow(const int width, const int height) {
    auto pRunner = Runner::getInstance();
    pRunner->resizeWindow(width, height);
}

void setElement(std::string& elementJson) {
    auto pRunner = Runner::getInstance();

    pRunner->setElement(elementJson);
}

void patchElement(int id, std::string& elementJson) {
    auto pRunner = Runner::getInstance();

    pRunner->patchElement(id, elementJson);
}

void elementInternalOp(int id, std::string& elementJson) {
    auto pRunner = Runner::getInstance();

    pRunner->elementInternalOp(id, elementJson);
}

void setChildren(int id, std::string& childrenIds) {
    auto pRunner = Runner::getInstance();
    // todo: use array of numbers instead of parsing JSON
    pRunner->setChildren((int)id, JsonToVector<int>(childrenIds));
}

void appendChild(int parentId, int childId) {
    auto pRunner = Runner::getInstance();
    
    pRunner->appendChild(parentId, childId);
}

std::string getChildren(int id) {
    auto pRunner = Runner::getInstance();
    
    return IntVectorToJson(pRunner->getChildren(id)).dump();
}

void appendTextToClippedMultiLineTextRenderer(int id, std::string& data) {
    auto pRunner = Runner::getInstance();

    pRunner->appendTextToClippedMultiLineTextRenderer(id, data);
}

std::string getStyle() {
    auto pRunner = Runner::getInstance();
    
    return pRunner->getStyle();
}

void patchStyle(std::string& styleDef) {
    auto pRunner = Runner::getInstance();
    
    pRunner->patchStyle(styleDef);
}

void setDebug(const bool debug) {
    auto pRunner = Runner::getInstance();

    pRunner->setDebug(debug);
}

void showDebugWindow() {
    auto pRunner = Runner::getInstance();

    pRunner->showDebugWindow();
}

int run()
{
    auto pRunner = Runner::getInstance();

    pRunner->run();

    return 0;
}

std::thread uiThread;


std::thread nativeThread;

/**
 * [0] assets base path
 * [1] raw font definitions (stringified JSON)
 * [2] raw style override definitions (stringified JSON)
 * [3] onInit function
 * [4] onTextChanged function
 * [5] onComboChanged function
 * [6] onNumericValueChanged function
 * [7] OnBooleanValueChanged function
 * [8] OnMultipleNumericValuesChanged function
 * [9] OnClick function
 */
static void init(
    const std::string& assetsBasePath,
    const std::string& rawFontDefinitions,
    const std::string& rawStyleOverrideDefinitions,
    OnInitCb& onInit,
    OnTextChangedCb& onTextChanged,
    OnComboChangedCb& onComboChanged,
    OnNumericValueChangedCb& onNumericValueChanged,
    OnBooleanValueChangedCb& onBooleanValueChanged,
    OnMultipleNumericValuesChangedCb& onMultipleNumericValuesChanged,
    OnClickCb& onClick
    ) {
    auto pRunner = Runner::getInstance();

    pRunner->SetAssetsBasePath(assetsBasePath);
    pRunner->SetRawFontDefs(rawFontDefinitions);
    pRunner->SetRawStyleOverridesDefs(rawStyleOverrideDefinitions);

    pRunner->SetHandlers(
        onInit,
        onTextChanged,
        onComboChanged,
        onNumericValueChanged,
        onBooleanValueChanged,
        onMultipleNumericValuesChanged,
        onClick
    );

    pRunner->init();

    uiThread = std::thread(run);
    uiThread.detach();
}

int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE(xframes, m) {
    m.doc() = R"pbdoc(
        Python bindings for XFrames
        -----------------------

        .. currentmodule:: xframes

        .. autosummary::
           :toctree: _generate

           init
    )pbdoc";

    m.def("init", &init);
    m.def("set_element", &setElement);
    m.def("patch_element", &patchElement);
    m.def("set_children", &setChildren);
    m.def("append_child", &appendChild);
    m.def("show_debug_window", &showDebugWindow);
    m.def("patch_style", &patchStyle);
    m.def("append_text_to_clipped_multi_line_text_renderer", &appendTextToClippedMultiLineTextRenderer);

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
