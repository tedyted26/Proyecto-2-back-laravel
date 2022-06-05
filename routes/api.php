<?php
use App\Http\Controllers\AuthController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;   

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/
$ruta_controllers = "App\Http\Controllers\\" ;

Route::middleware('auth:api')->get('/user', function (Request $request) {
        return $request->user();
    });

    Route::group([

        'middleware' => 'api',
        'prefix' => 'auth'
    
    ], function ($router) {
    
        Route::post('/login', 'App\Http\Controllers\AuthController@login');
        Route::post('/logout', 'App\Http\Controllers\AuthController@logout');
        Route::post('/refresh', 'App\Http\Controllers\AuthController@refresh');
        Route::post('/me', 'App\Http\Controllers\AuthController@me');
        Route::post('/register', 'App\Http\Controllers\AuthController@register');
    
    });
//Route::get('login', $ruta_controllers.);
//Route::get('logout', $ruta_controllers.);
//Route::get('refresh', $ruta_controllers.);
//Route::get('login', $ruta_controllers.);
