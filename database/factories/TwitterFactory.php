<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Twitter>
 */
class TwitterFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition()
    {
        return [
            "total_likes"=>$this->faker->numberBetween(0,1000000),
            "numero_tweets"=>$this->faker->numberBetween(5,500),
            "total_retweets"=>$this->faker->numberBetween(0,1000000),
            "resultado_analisis"=>$this->faker->randomFloat(4,-1.0,1.0),
            "busquedas_id"=>\App\Models\Busquedas::inRandomOrder()->first()->id
        ];
    }
}
