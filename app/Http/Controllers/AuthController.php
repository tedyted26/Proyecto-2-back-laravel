<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Auth;
use App\Http\Controllers\Controller;


use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use App\Models\User;
use App\Models\Busquedas;



class AuthController extends Controller
{
    /**
     * Create a new AuthController instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->middleware('auth:api', ['except' => ['login', 'register']]);
        
    }

    /**
     * Get a JWT via given credentials.
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function login()
    {
        $credentials = request(['email', 'password']);
        if (!$token = auth()->attempt($credentials)) {
            return response()->json(['error' => 'Unauthorized'], 401);
        }
        return $this->respondWithToken($token);
    }

    public function getAdminGraphicsData()
    {
        $out = new \Symfony\Component\Console\Output\ConsoleOutput();
        $out->writeln("Entrando a graficos");
        $lista_prov = ["A Coruña","Albacete","Alicante","Almería",
        "Asturias","Álava","Ávila","Badajoz","Baleares","Barcelona","Burgos","Cantabria",
        "Castellón","Ceuta","Ciudad Real","Cuenca","Cáceres","Cádiz",
        "Córdoba","Girona","Granada","Guadalajara","Guipúzcoa","Huelva","Huesca","Jaén",
        "La Rioja","Las Palmas","León","Lleida","Lugo","Madrid","Melilla","Murcia","Málaga",
        "Navarra","Ourense","Palencia","Pontevedra","SC. Tenerife","Salamanca","Segovia","Sevilla",
        "Soria","Tarragona","Teruel","Toledo","Valencia","Valladolid","Vizcaya","Zamora","Zaragoza"];
        $out->writeln("pre for");
        $lista_res = [];

        $out->writeln("minibusqueda");
        foreach ($lista_prov as $prov){
            try{
                $out->writeln($prov);
                $busqueda_q = Busquedas::select('*')->where("lugar", $prov)->orderBy('id', 'desc')->first();
                $out->writeln("medio post query");
                array_push($lista_res, $busqueda_q);
                $out->writeln("sale");
            }catch(Exception $ex){
                $out->writeln("error");
            }
        };
        $out->writeln("post for");
        $out->writeln($lista_res);
        return  json_encode($lista_res);
       
        
    }
    /**
     * Get the authenticated User.
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function me()
    {
        return response()->json(auth()->user());
    }

    /**
     * Log the user out (Invalidate the token).
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function logout()
    {
        auth()->logout();

        return response()->json(['message' => 'Successfully logged out']);
    }


    public function refresh()
    {
        return $this->respondWithToken(auth()->refresh());
    }


    protected function respondWithToken($token)
    {
        return response()->json([
            'access_token' => $token,
            'token_type' => 'bearer',
            'expires_in' => auth()->factory()->getTTL() * 60
        ]);
    }
    public function register(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'name' => 'required',
            'email' => 'required|string|email|max:100|unique:users',
            'password' => 'required|string|max:10',
             
        ]);
        if ($validator -> fails()){
            return response()->json($validator->errors()->toJson(), 400);
        }
        $user = User::create(array_merge(
            $validator -> validate(),
            ['password' => bcrypt($request->password)]
        ));
        return response()->json([
            'message'=>'Usuario registrado correctamente',
            'user'=> $user
        ], 201);
    }
}