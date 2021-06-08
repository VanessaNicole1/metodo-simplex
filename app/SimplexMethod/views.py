from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .maxi import Tableau

## EXAMPLE
##t = Tableau([-50,-80])
##t.add_constraint([1, 2], 120)
##t.add_constraint([1, 1], 90)
##print(t.solve())
# Create your views here.
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
        print(response)  # only for see how return data please delete this
        print(rta)
        
    return render(
        request, "sol.html", context={"solution": response, "response":rta, "tam": range(tamano), "x": range(varis)}
    )  # iter solution to present response

    # *******EXAMPLE OF RESPONSE**********
    # [
    #   {
    #   'iter': 0,
    #   'pivot': [-1, -1],
    #   'tableu': [
    #     [1.0, -50.0, -80.0, 0.0, 0.0, 0.0],
    #     [0.0, 1.0, 2.0, 1.0, 0.0, 120.0],
    #     [0.0, 1.0, 1.0, 0.0, 1.0, 90.0]
    #     ]
    #   },
    #   {
    #   'iter': 1, 'pivot': [3, 2],
    #   'tableu': [
    #     [1.0, -10.0, 0.0, 40.0, 0.0, 4800.0],
    #     [0.0, 0.5, 1.0, 0.5, 0.0, 60.0],
    #     [0.0, 0.5, 0.0, -0.5, 1.0, 30.0]
    #     ]
    #   },
    #   {
    #   'iter': 2,
    #   'pivot': [2, 3],
    #   'tableu': [[1.0, 0.0, 0.0, 30.0, 20.0, 5400.0], [0.0, 0.0, 1.0, 1.0, -1.0, 30.0], [0.0, 1.0, 0.0, -1.0, 2.0, 60.0]]
    #   }
    # ]
    #
    #
    #
    #

