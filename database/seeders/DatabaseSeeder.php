<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @return void
     */
    public function run()
    {
        // \App\Models\User::factory(10)->create();
        \App\Models\Admins::factory(5)->create();
        /*
        \App\Models\Busquedas::factory(10)->create();
        \App\Models\Noticias::factory(500)->create();
        \App\Models\Twitter::factory(20)->create();
        */
    }
}
