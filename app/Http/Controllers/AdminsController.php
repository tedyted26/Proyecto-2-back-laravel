<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Admins;

class AdminsController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        return Admins::orderBy('created_at', 'asc')->get();
    }
    public function index2(Request $request)
    {
        $out = new \Symfony\Component\Console\Output\ConsoleOutput();
        return response()->json(Admins::orderBy('created_at', 'asc')->get());
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $this->validate($request, [ //inputs are not empty or null
            'nombre' => 'required',
            'apellidos' => 'required',
            'correo' => 'required',
            'password' => 'required',
        ]);
  
        $admin = new Admins;
        $admin->nombre = $request->input('nombre'); //retrieving user inputs
        $admin->apellidos = $request->input('apellidos');  //retrieving user inputs
        $admin->correo = $request->input('correo'); //retrieving user inputs
        $admin->password = $request->input('password');  //retrieving user inputs

        $admin->save(); //storing values as an object
        return $admin; //returns the stored value if the operation was successful.
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        return Admins::findorFail($id);
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function edit($id)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        //
    }
}
