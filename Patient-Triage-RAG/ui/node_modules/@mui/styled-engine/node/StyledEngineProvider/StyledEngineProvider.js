"use strict";
'use client';

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault").default;
var _interopRequireWildcard = require("@babel/runtime/helpers/interopRequireWildcard").default;
Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = StyledEngineProvider;
var React = _interopRequireWildcard(require("react"));
var _propTypes = _interopRequireDefault(require("prop-types"));
var _react2 = require("@emotion/react");
var _cache = _interopRequireDefault(require("@emotion/cache"));
var _sheet = require("@emotion/sheet");
var _jsxRuntime = require("react/jsx-runtime");
// We might be able to remove this when this issue is fixed:
// https://github.com/emotion-js/emotion/issues/2790
const createEmotionCache = (options, CustomSheet) => {
  const cache = (0, _cache.default)(options);

  // Do the same as https://github.com/emotion-js/emotion/blob/main/packages/cache/src/index.js#L238-L245
  cache.sheet = new CustomSheet({
    key: cache.key,
    nonce: cache.sheet.nonce,
    container: cache.sheet.container,
    speedy: cache.sheet.isSpeedy,
    prepend: cache.sheet.prepend,
    insertionPoint: cache.sheet.insertionPoint
  });
  return cache;
};
let cache;
if (typeof document === 'object') {
  // Use `insertionPoint` over `prepend`(deprecated) because it can be controlled for GlobalStyles injection order
  // For more information, see https://github.com/mui/material-ui/issues/44597
  let insertionPoint = document.querySelector('[name="emotion-insertion-point"]');
  if (!insertionPoint) {
    insertionPoint = document.createElement('meta');
    insertionPoint.setAttribute('name', 'emotion-insertion-point');
    insertionPoint.setAttribute('content', '');
    const head = document.querySelector('head');
    if (head) {
      head.prepend(insertionPoint);
    }
  }
  /**
   * This is for client-side apps only.
   * A custom sheet is required to make the GlobalStyles API injected above the insertion point.
   * This is because the [sheet](https://github.com/emotion-js/emotion/blob/main/packages/react/src/global.js#L94-L99) does not consume the options.
   */
  class MyStyleSheet extends _sheet.StyleSheet {
    insert(rule, options) {
      if (this.key && this.key.endsWith('global')) {
        this.before = insertionPoint;
      }
      return super.insert(rule, options);
    }
  }
  cache = createEmotionCache({
    key: 'css',
    insertionPoint
  }, MyStyleSheet);
}
function StyledEngineProvider(props) {
  const {
    injectFirst,
    children
  } = props;
  return injectFirst && cache ? /*#__PURE__*/(0, _jsxRuntime.jsx)(_react2.CacheProvider, {
    value: cache,
    children: children
  }) : children;
}
process.env.NODE_ENV !== "production" ? StyledEngineProvider.propTypes = {
  /**
   * Your component tree.
   */
  children: _propTypes.default.node,
  /**
   * By default, the styles are injected last in the <head> element of the page.
   * As a result, they gain more specificity than any other style sheet.
   * If you want to override MUI's styles, set this prop.
   */
  injectFirst: _propTypes.default.bool
} : void 0;