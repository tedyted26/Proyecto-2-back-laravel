<?php

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

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

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



