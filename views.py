from django.shortcuts import render, redirect
from django.conf import settings
from .models import Idantifikasyon, Deplase, FinansTimoun, Rezidan
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Case, When, IntegerField,Subquery, OuterRef, FloatField, ExpressionWrapper, F
from django.http import JsonResponse
import plotly.express as px

# Create your views here.

@login_required
def index(request):
    menages = Idantifikasyon.objects.all()[:25]
    menages_total = Idantifikasyon.objects.all().count()
    menages_grannrivye_total = Idantifikasyon.objects.filter(komin='Grannrivyè').count()
    menages_senrafayel_total = Idantifikasyon.objects.filter(komin='Senrafayèl').count()
    menages_ferye_total = Idantifikasyon.objects.filter(komin='Ferye').count()
    menages_deplase = Deplase.objects.all()[:25]
    menages_finansTimoun = FinansTimoun.objects.all()[:25]
    menages_rezidan = Rezidan.objects.all()[:25]

   
    context = {
        'menages': menages,
       'menages_deplase': menages_deplase,
       'menages_finansTimoun': menages_finansTimoun,
       'menages_rezidan': menages_rezidan,
       'menages_total': menages_total,
       'menages_grannrivye_total': menages_grannrivye_total,
       'menages_senrafayel_total': menages_senrafayel_total,
       'menages_ferye_total': menages_ferye_total,
  
    }
    return render(request, 'index.html', context)

@login_required
def senrafayel(request):
    # if not request.user.is_authenticated:
    #     return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    # type de batiments à saint-raphael
    kalite_kay = Idantifikasyon.objects.filter(komin='Senrafayèl').values('kalite_kay').annotate(kantite=Count('kalite_kay'))
    kantite_kay = Idantifikasyon.objects.annotate(kantite=Count('kalite_kay'))

    x_kalite_kay = []
    y_kantite_kay = []

    for kay in kalite_kay:
        x_kalite_kay.append(kay['kalite_kay'])
        y_kantite_kay.append(kay['kantite']) 

    fig = px.bar(x=x_kalite_kay, y=y_kantite_kay,
                 title= 'Kalite kay',
                 labels={'x': 'Kalite Kay la', 'y': 'Ki Kantite'})
    chart_kalite_kay = fig.to_html()

  
    context = {
        'chart_kalite_kay': chart_kalite_kay,
        
    }
    return render(request, 'senrafayel.html', context)



@login_required
def ferye(request):
    # if not request.user.is_authenticated:
    #     return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    # type de batiments à saint-raphael
    kalite_kay = Idantifikasyon.objects.filter(komin='Ferye').values('kalite_kay').annotate(kantite=Count('kalite_kay'))
    kantite_kay = Idantifikasyon.objects.annotate(kantite=Count('kalite_kay'))

    x_kalite_kay = []
    y_kantite_kay = []

    for kay in kalite_kay:
        x_kalite_kay.append(kay['kalite_kay'])
        y_kantite_kay.append(kay['kantite']) 

    fig = px.bar(x=x_kalite_kay, y=y_kantite_kay,
                 title= 'Kalite kay',
                 labels={'x': 'Kalite Kay la', 'y': 'Ki Kantite'})
    chart_kalite_kay = fig.to_html()

    
    context = {
        'chart_kalite_kay': chart_kalite_kay,
    
    return render(request, 'ferye.html', context)


@login_required
def grannrivye(request):
    # if not request.user.is_authenticated:
    #     return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    # type de batiments à saint-raphael
    kalite_kay = Idantifikasyon.objects.filter(komin='Grannrivyè').values('kalite_kay').annotate(kantite=Count('kalite_kay'))
    kantite_kay = Idantifikasyon.objects.annotate(kantite=Count('kalite_kay'))

    x_kalite_kay = []
    y_kantite_kay = []

    for kay in kalite_kay:
        x_kalite_kay.append(kay['kalite_kay'])
        y_kantite_kay.append(kay['kantite']) 

    fig = px.bar(x=x_kalite_kay, y=y_kantite_kay,
                 title= 'Kalite kay',
                 labels={'x': 'Kalite Kay la', 'y': 'Ki Kantite'})
    chart_kalite_kay = fig.to_html()

    # Statut matrimonial des chefs de menage
    statut_matrimonial = Idantifikasyon.objects.filter(komin='Grannrivyè').values('eta_sivil_chef_kay').annotate(kantite=Count('eta_sivil_chef_kay'))
   
    matrimonial_value = []
    matrimonial_names = []
    for chef_kay in statut_matrimonial:
        matrimonial_value.append(chef_kay['kantite'])
        matrimonial_names.append(chef_kay['eta_sivil_chef_kay'])


    fig_matrimonial = px.pie(statut_matrimonial, values=matrimonial_value, names=matrimonial_names)
    chart_matrimonial = fig_matrimonial.to_html()


    # Revenu mensuel des chefs de ménages
    revenus = Idantifikasyon.objects.filter(komin='Grannrivyè').values('kob_mwa_chefkay').annotate(kantite=Count('kob_mwa_chefkay'))
    x_kobmwa = []
    y_kobmwa = []

    for chef_kay in revenus:
        x_kobmwa.append(chef_kay['kob_mwa_chefkay'])
        y_kobmwa.append(chef_kay['kantite'])

    fig_revenus = px.bar(x=x_kobmwa, y=y_kobmwa, title='Revenu mensuel des chefs de ménages', 
                          labels={'x': 'revenus', 'y': 'nombre de ménages'},)
    chart_revenu = fig_revenus.to_html()


    # frequence ramassage d'ordures
    ramassages = Idantifikasyon.objects.filter(komin='Grannrivyè').values('ramase_fatra_mwa').annotate(kantite=Count('ramase_fatra_mwa'))
    ramase_value = []
    ramase_name = []

    for chef_kay in ramassages:
        ramase_value.append(chef_kay['kantite'])
        ramase_name.append(chef_kay['ramase_fatra_mwa'])

    fig_ramase_fatra = px.pie(ramassages, values=ramase_value, names=ramase_name) 
    chart_ramase_fatra = fig_ramase_fatra.to_html()


    # -- 16.	Raison du travail des enfants
    travay_timoun_value = []
    travay_timoun_name = []

    rezon_travay_timoun = Idantifikasyon.objects.filter(komin='Grannrivyè').values('rezon_aktivite_ekonomi_timoun').exclude(rezon_aktivite_ekonomi_timoun__isnull=True).annotate(kantite=Count('rezon_aktivite_ekonomi_timoun'))

    for timoun in rezon_travay_timoun:
        travay_timoun_value.append(timoun['kantite'])
        travay_timoun_name.append(timoun['rezon_aktivite_ekonomi_timoun'])

    fig_travay_timoun = px.pie(rezon_travay_timoun, values=travay_timoun_value, names=travay_timoun_name)
    chart_travay_timoun = fig_travay_timoun.to_html()


    # 18.	Statut d'occupation de votre logement
    okipasyon_kay = Idantifikasyon.objects.filter(komin='Grannrivyè').values('lyen_chefkay_ak_kay').annotate(kantite=Count('lyen_chefkay_ak_kay'))
    x_okipasyon_kay = []
    y_okipasyon_kay = []
    for chef_kay in okipasyon_kay:
        x_okipasyon_kay.append(chef_kay['lyen_chefkay_ak_kay'])
        y_okipasyon_kay.append(chef_kay['kantite'])

    fig_okipasyon_kay = px.bar(x=x_okipasyon_kay, y=y_okipasyon_kay, title='Statut d\'occupation du logement', 
                          labels={'x': 'Occupation du logement', 'y': 'nombre de ménages'},) 
    chart_okipasyon_kay = fig_okipasyon_kay.to_html()


    # Mode d'approvisionnement en eau de boisson
    dlo_potab = Idantifikasyon.objects.filter(komin='Grannrivyè').values('mwayen_dlo_potab').exclude(mwayen_dlo_potab__isnull=True).annotate(kantite=Count('mwayen_dlo_potab'))
    x_dlo_potab = []
    y_dlo_potab = []
    for menaj in dlo_potab:
        x_dlo_potab.append(menaj['mwayen_dlo_potab'])
        y_dlo_potab.append(menaj['kantite'])
    
    fig_dlo_potab = px.bar(x=x_dlo_potab,y=y_dlo_potab, title='Mode d\'approvisionnement en eau de boisson',
                           labels={'x': 'Approvisionnement en eau', 'y': 'nombre de ménages'},)
    chart_dlo_potab = fig_dlo_potab.to_html() 


    # -- 20.	Source d'éclairage du ménage ?
    kouran_menaj = Idantifikasyon.objects.filter(komin='Grannrivyè').values('mwayen_limye_kouran').exclude(mwayen_limye_kouran__isnull=True).annotate(kantite=Count('mwayen_limye_kouran'))
    x_kouran = []
    y_kouran = []
    for menaj in kouran_menaj:
        x_kouran.append(menaj['mwayen_limye_kouran'])
        y_kouran.append(menaj['kantite'])

    fig_kouran_menaj = px.bar(x=x_kouran, y=y_kouran, title='Source d\'éclairage du ménage',
                              labels={'x': 'Source d\'éclairage', 'y': 'Menages'})
    chart_kouran_menaj = fig_kouran_menaj.to_html()


    # -- 21.	Combustible pour la cuisine
    kuit_manje = Idantifikasyon.objects.filter(komin='Grannrivyè').values('mwayen_dife_kuit_manje').exclude(mwayen_dife_kuit_manje__isnull=True).annotate(kantite=Count('mwayen_dife_kuit_manje'))
    x_kuit_manje = []
    y_kuit_manje = []
    for menaj in kuit_manje:
        x_kuit_manje.append(menaj['mwayen_dife_kuit_manje'])
        y_kuit_manje.append(menaj['kantite'])

    fig_kuit_manje = px.bar(x=x_kuit_manje, y=y_kuit_manje, title='Combustible pour la cuisine',
                              labels={'x': 'Combustible', 'y': 'Menages'})
    chart_kuit_manje = fig_kuit_manje.to_html()

    # -- 22.	Type de toilettes les membres de votre ménage
    kalite_twalet = Idantifikasyon.objects.filter(komin='Grannrivyè').values('mwayen_fe_bezwen').exclude(mwayen_fe_bezwen__isnull=True).annotate(kantite=Count('mwayen_fe_bezwen'))
    kalite_twalet_name = []
    kalite_twalet_value = []
    for menaj in kalite_twalet:
        kalite_twalet_name.append(menaj['mwayen_fe_bezwen'])
        kalite_twalet_value.append(menaj['kantite'])

    fig_kalite_twalet = px.pie(kalite_twalet, values=kalite_twalet_value, names=kalite_twalet_name)
    chart_kalite_twalet = fig_kalite_twalet.to_html()


    # -- 23.	Intention du ménage de déménager
    menaj_vle_demenaje = Idantifikasyon.objects.filter(komin='Grannrivyè').values('fanmi_vle_kite_kay').annotate(kantite=Count('fanmi_vle_kite_kay'))
    vle_kite_name = []
    vle_kite_value = []
    for menaj in menaj_vle_demenaje:
        vle_kite_name.append(menaj['fanmi_vle_kite_kay'])
        vle_kite_value.append(menaj['kantite'])

    fig_vle_demenaje = px.pie(menaj_vle_demenaje, values=vle_kite_value, names=vle_kite_name)
    chart_vle_demenaje = fig_vle_demenaje.to_html()


    # -- 24.	Nombre de personnes (membres du ménage) ayant laissé leur lieu de résidence
    kantite_deplase = Idantifikasyon.objects.filter(komin='Grannrivyè').values('kantite_moun_deplase').aggregate(Sum('kantite_moun_deplase'))
    kantite_moun_deplase = kantite_deplase['kantite_moun_deplase__sum']


    # -- 26.	Raison de déplacement
    deplase_Grannrivye = Idantifikasyon.objects.filter(komin='Grannrivyè').values('id_idantifikasyon')
    rezon_deplase = Deplase.objects.filter(id_idantifikasyon__in=Subquery(deplase_Grannrivye)).values('rezon_deplase_chanje_kay').annotate(kantite=Count('rezon_deplase_chanje_kay'))
    rezon_deplase_name = []
    rezon_deplase_value = []
    for menaj in rezon_deplase:
        rezon_deplase_name.append(menaj['rezon_deplase_chanje_kay'])
        rezon_deplase_value.append(menaj['kantite'])
    
    fig_rezon_deplase = px.pie(rezon_deplase, values=rezon_deplase_value, names=rezon_deplase_name)

    chart_rezon_deplase = fig_rezon_deplase.to_html()


    # -- 27.	Lieu de l’installation (nouveau)
    deplase_Grannrivye = Idantifikasyon.objects.filter(komin='Grannrivyè').values('id_idantifikasyon')
    zon_deplase = Deplase.objects.filter(id_idantifikasyon__in=Subquery(deplase_Grannrivye)).values('kote_deplase_ale').annotate(kantite=Count('kote_deplase_ale'))

    zon_deplase_name = []
    zon_deplase_value = []

    for menaj in zon_deplase:
        zon_deplase_name.append(menaj['kote_deplase_ale'])
        zon_deplase_value.append(menaj['kantite'])

    fig_zon_deplase = px.pie(zon_deplase, values=zon_deplase_value, names=zon_deplase_name)

    chart_zon_deplase = fig_zon_deplase.to_html()

    context = {
        'chart_kalite_kay': chart_kalite_kay,
        'chart_matrimonial': chart_matrimonial,
        'chart_revenu': chart_revenu,
        'chart_ramase_fatra': chart_ramase_fatra,
        'chart_travay_timoun': chart_travay_timoun,
        'chart_okipasyon_kay': chart_okipasyon_kay,
        'chart_dlo_potab': chart_dlo_potab,
        'chart_kouran_menaj': chart_kouran_menaj,
        'chart_kuit_manje': chart_kuit_manje,
        'chart_kalite_twalet': chart_kalite_twalet,
        'chart_vle_demenaje': chart_vle_demenaje,
        'kantite_moun_deplase': kantite_moun_deplase,
        'chart_rezon_deplase': chart_rezon_deplase,
        'chart_zon_deplase': chart_zon_deplase,
    }
    return render(request, 'grannrivye.html', context)

def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'registration/register.html', {'form': form})
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Registration completed successfully')
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'registration/register.html', {'form':form})
        

# logout
def signout(request):
    logout(request)
    messages.success(request, 'You logged out successfully')
    return redirect('login')
