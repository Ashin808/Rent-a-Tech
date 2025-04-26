from django.shortcuts import render

# Create your views here.
def add(request):
    if request.method=='POST':
        num1=int(request.POST.get('txt_num1'))
        num2=int(request.POST.get('txt_num2'))
        result=num1+num2
        return render(request,'Basics/Add.html',{'sum':result})
    else:
        return render(request,'Basics/Add.html')

def largest(request):
    if request.method == 'POST':
        num1 = int(request.POST.get('txt_num1'))
        num2 = int(request.POST.get('txt_num2'))
        if num1 > num2:
            result = num1
        elif num2 > num1:
            result = num2
        else:
            result = "both are equal"
        return render(request, 'Basics/Largest.html', {'largest': result})
    else:
        return render(request, 'Basics/Largest.html')


def Calculator(request):
    if request.method=='POST':
        a=int(request.POST.get('txt_num1'))
        b=int(request.POST.get('txt_num2'))
        btn=request.POST.get("btn")
        if btn=='+':
            result=a+b
        elif btn=='-':
            result=a-b    
        elif btn=='*':
            result=a*b  
        elif btn=='/':
            result=a/b  
        return render(request,'Basics/Calculator.html',{'res':result})
    else:
        return render(request,'Basics/Calculator.html')     


def largestandsmallest(request):
    # if request.method == 'POST':
    #     num1 = int(request.POST.get('txt_num1'))
    #     num2 = int(request.POST.get('txt_num2'))
    #     if num1 > num2:
    #         result = num1
    #     elif num2 > num1:
    #         result = num2
    #     else:
    #         result = "both are equal"
    # elif:
    #     if num1 < num2:
    #             result = f"Smallest: {num1}"
    #         elif num2 < num1:
    #             result = f"Smallest: {num2}"
    #         else:
    #             result = "Both are equal (Smallest)"
    #     return render(request, 'Basics/largestsmallest.html', {'result': result})
    # else:
        return render(request, 'Basics/largestsmallest.html')