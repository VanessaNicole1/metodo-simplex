from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .maxi import Tableau

variables = 2
restricts = 2


def index(request):
    if request.method == "GET":
        return render(request, "index2.html")
    elif request.method == "POST":
        variables = request.POST.get("n_variables")
        restricciones = request.POST.get("n_restriccion")
        return HttpResponseRedirect(
            "/calcular?variables=" + variables + "&restricciones=" + restricciones
        )


def calculo(request):
    global variables, restricts
    if request.method == "GET":
        variables = int(request.GET.get("variables"))
        restricts = int(request.GET.get("restricciones"))
        return render(
            request,
            "index.html",
            context={"v": range(variables), "r": range(restricts)},
        )
    elif request.method == "POST":
        objetive = []
        for i in range(variables):
            objetive.append(float(request.POST.get("obj-" + str(i))) * -1)

        tabla = Tableau(objetive)

        for j in range(restricts):
            restric = []
            for i in range(variables):
                restric.append(float(request.POST.get("res" + str(j) + "-" + str(i))))
            rta = float(request.POST.get("res" + str(j) + "-rta"))
            tabla.add_constraint(restric, rta)

        response, rta  = tabla.solve()
        tamano = restricts
        varis = variables
        
    return render(
        request, "sol.html", context={"solution": response, "response":rta, "tam": range(tamano), "x": range(varis)}
    )  
