<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Noticias>
 */
class NoticiasFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition()
    {
        
        return [
            "url"=>$this->faker->url,
            "titulo"=>$this->faker->word,
            "subtitulo"=>$this->faker->sentence,
            "fecha_noticia"=>$this->faker->date,
            "resultado"=>$this->faker->randomElement([-1, 0, 1]),
            "busquedas_id"=>\App\Models\Busquedas::inRandomOrder()->first()->id
        ];
    }
}
