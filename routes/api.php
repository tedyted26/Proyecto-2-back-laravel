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

//Route::get('admins', $ruta_controllers.'AdminsController@index');
//Route::post('admins', $ruta_controllers.'AdminsController@index2');
//Route::get('admins/{id}', $ruta_controllers.'AdminsController@show');
//Route::post('busquedas', $ruta_controllers.'BusquedasController@getSearch');
//Route::get('busquedas', $ruta_controllers.'BusquedasController@index');
//Route::get('busquedas/{id}', $ruta_controllers.'BusquedasController@show');
Route::group(['middleware' => ['cors']], function () {
    $ruta_controllers = "App\Http\Controllers\\" ;
    //Rutas a las que se permitirá acceso
    Route::get('admins', $ruta_controllers.'AdminsController@index');
    Route::post('admins', $ruta_controllers.'AdminsController@index2');
    Route::get('admins/{id}', $ruta_controllers.'AdminsController@show');
    Route::post('busquedas', $ruta_controllers.'BusquedasController@getSearch');
    Route::get('busquedas', $ruta_controllers.'BusquedasController@index');
    Route::get('busquedas/{id}', $ruta_controllers.'BusquedasController@show');
});



