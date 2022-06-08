<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('config', function (Blueprint $table) {
            $table->id();
            $table->string("contact_mail");
            $table->string("contact_num");
            $table->integer("is_abc");
            $table->integer("is_20min");
            $table->integer("is_elpais");
            $table->integer("is_lasexta");
            $table->integer("is_lavang");
            $table->integer("is_larazon");
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('config');
    }
};
