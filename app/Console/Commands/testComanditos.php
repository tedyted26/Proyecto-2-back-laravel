<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Storage;

class testComanditos extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'command:runtest';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command command for example';


    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $this->info("Custom task started");
        Storage::disk('local')->put('example.txt', "Hola");
        dd("testeito");
        return 0;
    }
}
