<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Busquedas extends Model
{
    use HasFactory;
    protected $table = 'busquedas';
    protected $fillable = [
        'lugar',
        'fecha_busqueda',
        'visitas_totales',
        'resultado_odio',
    ];
}
