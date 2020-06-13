"use strict";

// Imports
var { src, dest, series, parallel, watch } = require("gulp");
var argv = require("minimist")(process.argv.slice(2));
var pkg = require("./package.json");
var header = require("gulp-header");
var del = require("del");
var sass = require("gulp-sass");
var postcss = require("gulp-postcss");
var postcssPresetEnv = require("postcss-preset-env");
var cssnano = require("cssnano");
var stylelint = require("gulp-stylelint");
var browserSync = require("browser-sync").create();

// Vendor settings
sass.compiler = require("node-sass");

// Banner for file headers
var banner = [
  "/**",
  " * <%= pkg.name %> v<%= pkg.version %>",
  " * @author <%= pkg.author %>",
  " */",
  "",
].join("\n");

// Settings
var settings = {
  production: !!argv.production,
  clean: true,
  copy: true,
  styles: true,
  reload: true,
};

// Paths

var paths = {
  input: "website/static/src/",
  output: "website/static/dist/",
};

var copyPaths = {
  input: paths.input + "copy/**/*",
  output: paths.output,
};

var stylesPaths = {
  input: [
    paths.input + "scss/**/*.scss",
    "!" + paths.input + "scss/vendors/**",
  ],
  output: paths.output + "css/",
};

var templatePath = "**/templates/**"

// Functions

function cleanDist(done) {
  // Make sure this feature is activated before running
  if (!settings.clean) return done();

  // Clean the dist folder
  del.sync([paths.output]);

  // Signal completion
  return done();
}

// Copy static files into output folder
function copyFiles(done) {
  // Make sure this feature is activated before running
  if (!settings.copy) return done();

  // Copy static files
  return src(copyPaths.input).pipe(dest(copyPaths.output));
}

function buildStyles(done) {
  // Make sure this feature is activated before running
  if (!settings.styles) return done();

  // Process styles
  return src(stylesPaths.input, settings.production ? {} : { sourcemaps: true })
    .pipe(sass().on("error", sass.logError))
    .pipe(postcss(settings.production ? [cssnano(), postcssPresetEnv()] : [postcssPresetEnv()]))
    .pipe(header(banner, { pkg: pkg }))
    .pipe(dest(stylesPaths.output, settings.production ? {} : { sourcemaps: "." }));
}

function lintStyles(done) {
  // Make sure this feature is activated before running
  if (!settings.styles) return done();

  return src(stylesPaths.input).pipe(
    stylelint({
      failAfterError: false,
      reporters: [{ formatter: "string", console: true }],
    })
  );
}

// Watch for changes to the src directory
function startServer(done) {
  // Make sure this feature is activated before running
  if (!settings.reload) return done();

  // Initialize BrowserSync
  browserSync.init({ proxy: "127.0.0.1:8000" });

  // Signal completion
  done();
}

// Reload the browser when files change
var reloadBrowser = function (done) {
  if (!settings.reload) return done();
  browserSync.reload();
  done();
};

// Watch for changes
function watchSource(done) {
  watch([paths.input, templatePath], series(exports.default, reloadBrowser));
  done();
};

// Default task
// gulp
exports.default = series(
  cleanDist,
  parallel(copyFiles, buildStyles, lintStyles)
);

// Watch and reload
// gulp watch
exports.watch = series(
  exports.default,
  startServer,
  watchSource
);
