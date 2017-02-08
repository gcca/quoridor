import os
import json


BS_CONFIG = '''{
  "server": {
    "baseDir": "src",
    "routes": {
      "/node_modules": "node_modules"
    }
  }
}
'''


TS_CONFIG = '''{
  "compilerOptions": {
    "target": "es5",
    "module": "commonjs",
    "moduleResolution": "node",
    "sourceMap": true,
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true,
    "lib": [ "es2015", "dom" ],
    "noImplicitAny": true,
    "suppressImplicitAnyIndexErrors": true
  }
}
'''


TS_CONFIG_AOT = '''{
  "compilerOptions": {
    "target": "es5",
    "module": "es2015",
    "moduleResolution": "node",
    "sourceMap": true,
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true,
    "lib": ["es2015", "dom"],
    "noImplicitAny": true,
    "suppressImplicitAnyIndexErrors": true
  },
  "files": [
    "src/app/app.module.ts",
    "src/main-aot.ts"
  ],
  "angularCompilerOptions": {
    "genDir": "aot",
    "skipMetadataEmit" : true
  }
}
'''


ROLLUP = '''import rollup      from 'rollup';
import nodeResolve from 'rollup-plugin-node-resolve';
import commonjs    from 'rollup-plugin-commonjs';
import uglify      from 'rollup-plugin-uglify';


export default {
  entry: 'src/main-aot.js',
  dest: 'src/build.js',
  sourceMap: false,
  format: 'iife',
  onwarn: function(warning) {
    if (warning.code === 'THIS_IS_UNDEFINED') { return; }
    if (warning.indexOf("The 'this' keyword is equivalent to 'undefined'") > -1) {
      return;
    }
    console.warn(warning.message);
  },
  plugins: [
    nodeResolve({jsnext: true, module: true}),
    commonjs({
      include: 'node_modules/rxjs/**'
    }),
    uglify()
  ]
}
'''


DIST_FILES = '''var fs = require('fs');


if (!fs.existsSync('dist')) {
  fs.mkdirSync('dist');
}


var resources = [
	'node_modules/core-js/client/shim.min.js',
	'node_modules/zone.js/dist/zone.min.js',
  'src/build.js'
];

resources.map(function(f) {
	var path = f.split('/');
	var t = 'dist/' + path[path.length-1];
	fs.createReadStream(f).pipe(fs.createWriteStream(t));
});


var index = `<!DOCTYPE html>
<html>
  <head>
    <base href="/">
    <title>CiX</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="styles.css">
    <script src="shim.min.js"></script>
    <script src="zone.min.js"></script>
    <script>window.module = 'aot';</script>
  </head>
  <body>
    <cix-app>Loading...</cix-app>
  </body>
  <script src="build.js"></script>
</html>
`;

fs.writeFile('dist/index.html', index, function(e) {
  if (e) {
    console.log('Error creating index.html:');
    console.log(e);
  }
});
'''


INDEX_HTML = '''<!DOCTYPE html>
<html>
  <head>
    <title>CiX Angular2</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <base href="/">
    <link rel="stylesheet" href="styles.css">

    <script src="node_modules/core-js/client/shim.min.js"></script>

    <script src="node_modules/zone.js/dist/zone.js"></script>
    <script src="node_modules/systemjs/dist/system.src.js"></script>

    <script src="systemjs.config.js"></script>
    <script>
      System.import('main.js').catch(function(err){ console.error(err); });
    </script>
  </head>

  <body>
    <cix-app>Loading AppComponent content here ...</cix-app>
  </body>
</html>
'''


MAIN_TS = '''import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module';


platformBrowserDynamic().bootstrapModule(AppModule);
'''


MAIN_AOT_TS = '''
import { platformBrowser } from '@angular/platform-browser';

import { AppModuleNgFactory } from '../aot/src/app/app.module.ngfactory';


platformBrowser().bootstrapModuleFactory(AppModuleNgFactory);
'''


SYSTEMJS = '''/**
 * System configuration
 */
(function (global) {
  System.config({
    paths: {
      // paths serve as alias
      'npm:': 'node_modules/'
    },
    // map tells the System loader where to look for things
    map: {
      // our app is within the app folder
      app: 'app',

      // angular bundles
      '@angular/core': 'npm:@angular/core/bundles/core.umd.js',
      '@angular/common': 'npm:@angular/common/bundles/common.umd.js',
      '@angular/compiler': 'npm:@angular/compiler/bundles/compiler.umd.js',
      '@angular/platform-browser': 'npm:@angular/platform-browser/bundles/platform-browser.umd.js',
      '@angular/platform-browser-dynamic': 'npm:@angular/platform-browser-dynamic/bundles/platform-browser-dynamic.umd.js',
      '@angular/http': 'npm:@angular/http/bundles/http.umd.js',
      '@angular/router': 'npm:@angular/router/bundles/router.umd.js',
      '@angular/forms': 'npm:@angular/forms/bundles/forms.umd.js',

      // other libraries
      'rxjs':                      'npm:rxjs',
      'angular-in-memory-web-api': 'npm:angular-in-memory-web-api/bundles/in-memory-web-api.umd.js'
    },
    // packages tells the System loader how to load when no filename and/or no extension
    packages: {
      app: {
        main: './main.js',
        defaultExtension: 'js'
      },
      rxjs: {
        defaultExtension: 'js'
      }
    }
  });
})(this);
'''


APP_MODULE = '''import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';

import { AppComponent } from './app.component';


@NgModule({
  imports:      [ BrowserModule, FormsModule ],
  declarations: [ AppComponent ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
'''


APP_COMPONENT = '''import { Component } from '@angular/core';


@Component({
  selector: 'cix-app',
  template: '<h1>Cix-App</h1>'
})
export class AppComponent  { }
'''


class Unit:

    before = ['typescript', 'src']

    def start(self):
        package_path = os.path.join(self.destination, 'package.json')
        with open(package_path) as package_file:
            package = json.load(package_file)

        package['dependencies']['@angular/common'] = '~2.4.0'
        package['dependencies']['@angular/compiler'] = '~2.4.0'
        package['dependencies']['@angular/core'] = '~2.4.0'
        package['dependencies']['@angular/forms'] = '~2.4.0'
        package['dependencies']['@angular/http'] = '~2.4.0'
        package['dependencies']['@angular/platform-browser'] = '~2.4.0'
        package['dependencies']['@angular/platform-browser-dynamic'] = '~2.4.0'
        package['dependencies']['angular-in-memory-web-api'] = '~0.2.4'

        package['dependencies']['@angular/compiler-cli'] = '^2.4.6'
        package['dependencies']['@angular/platform-server'] = '^2.4.6'

        package['devDependencies']['rollup'] = '^0.41.4'
        package['devDependencies']['rollup-plugin-commonjs'] = '^7.0.0'
        package['devDependencies']['rollup-plugin-node-resolve'] = '^2.0.0'
        package['devDependencies']['rollup-plugin-uglify'] = '^1.0.1'

        package['scripts']['build:aot'] = 'ngc -p tsconfig-aot.json && rollup -c rollup-config.js'
        package['scripts']['dist'] = 'npm run build:aot && node scripts/dist-files.js'

        with open(package_path, 'w') as package_file:
            json.dump(package, package_file, indent=2)


        SRC_PATH = os.path.join(self.destination, 'src')
        SCRIPTS_PATH = os.path.join(self.destination, 'scripts')
        APP_PATH = os.path.join(SRC_PATH, 'app')

        dump(self.destination, 'bs-config.json', BS_CONFIG)
        dump(self.destination, 'tsconfig-aot.json', TS_CONFIG_AOT)
        dump(self.destination, 'rollup-config.js', ROLLUP)

        dump(SRC_PATH, 'tsconfig.json', TS_CONFIG)
        dump(SRC_PATH, 'index.html', INDEX_HTML)
        dump(SRC_PATH, 'systemjs.config.js', SYSTEMJS)
        dump(SRC_PATH, 'main.ts', MAIN_TS)
        dump(SRC_PATH, 'main-aot.ts', MAIN_AOT_TS)

        os.mkdir(SCRIPTS_PATH)
        dump(SCRIPTS_PATH, 'dist-files.js', DIST_FILES)

        os.mkdir(APP_PATH)
        dump(APP_PATH, 'app.module.ts', APP_MODULE)
        dump(APP_PATH, 'app.component.ts', APP_COMPONENT)

        print('Angular2 created')


def dump(basepath, filename, s):
    path = os.path.join(basepath, filename)
    with open(path, 'w') as file_dest:
        file_dest.write(s)

