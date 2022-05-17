<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Admins>
 */
class AdminsFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition()
    {
        $gender = $this->faker->randomElement(['male', 'female']);
        return [
            "nombre"=>$this->faker->name($gender),
            "apellidos"=>$this->faker->firstName($gender),
            "correo"=>$this->faker->email,
            "password"=>$this->faker->password,
        ];
    }
}
