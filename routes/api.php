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
$ruta_controllers = "App\Http\Controllers\\" ;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::get('admins', $ruta_controllers.'AdminsController@index');
Route::get('admins/{id}', $ruta_controllers.'AdminsController@show');
Route::get('busquedas', $ruta_controllers.'BusquedasController@index');
Route::get('busquedas/{id}', $ruta_controllers.'BusquedasController@show');
Route::get('noticias', $ruta_controllers.'NoticiasController@index');
Route::get('noticias/{id}', $ruta_controllers.'NoticiasController@show');
Route::get('twitter', $ruta_controllers.'TwitterController@index');
Route::get('twitter/{id}', $ruta_controllers.'TwitterController@show');
