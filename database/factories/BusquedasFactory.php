<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Busquedas>
 */
class BusquedasFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition()
    {
        return [
            "fecha_busqueda"=>$this->faker->date,
            "lugar"=>$this->faker->city,
            "visitas_totales"=>$this->faker->numberBetween(0,1000000),
            "resultado_odio"=>$this->faker->randomFloat(4,-1.0,1.0),
        ];
    }
}
