from django.http import HttpResponse, HttpResponseRedirect # noqa: 401
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

from .models import Status
from .forms import StatusForm

def index(request):
  d = {
      'Statuses': Status.objects.order_by('-id'),
  }
  return render(request, 'polls/index.html', d)

def add(request):
  form = StatusForm(request.POST or None)
  if form.is_valid():
    Status.objects.create(**form.cleaned_data)
    return redirect('polls:index')

  d = {
      'form': form,
  }
  return render(request, 'polls/edit.html', d)
  
def edit(request, pk):
  status = get_object_or_404(Status, pk=pk)
  if request.method == 'POST':
      form = StatusForm(request.POST, instance=status)
      if form.is_valid():
          status.hp = form.cleaned_data['hp']
          status.mp = form.cleaned_data['mp']
          status.event = form.cleaned_data['event']
          status.ap = status.hp * status.mp/100
          status.save()
          return redirect('polls:index')
  else:
      # GETリクエスト（初期表示）時はDBに保存されているデータをFormに結びつける
      form = StatusForm(instance=status)
  d = {
      'form': form,
  }

  return render(request, 'polls/edit.html', d)

def apcalc(request):
  #calc2.htmlに入力したものを計算して登録
  rStatus = Status.objects.order_by('id').reverse()[:1]#過去1回分のレコードを抽出
  p1ap = rStatus[0].ap#1つ前の答え
  p1hp = rStatus[0].hp
  p1mp = rStatus[0].mp
  p1ev = rStatus[0].event
  p1tm = rStatus[0].updated_at
  
  if request.method == 'POST':#これをしないとcalc.htmlを開いたときに勝手にPOSTしようとする
      ihp = int(request.POST['hp'])
      imp = int(request.POST['mp'])
      iap = ihp * imp/100
      ievent = str(request.POST['event'])
#      clossap = iap - p1ap
#      cdmg = ihp - p1hp
#      cusemp = imp - p1mp
#      cbehavior = str(p1ev)
      #now= datetime.now()
      #term = now.timestamp() - p1tm.timestamp() #DateTimeFieldに直したい
  #答えを新しいレコードに記録
      Status.objects.create(ap=iap, hp=ihp, mp=imp, event=ievent)
      #r2Status = Status.objects.order_by('id').reverse()[:1]#過去1回分のレコードを抽出
      #tm = r2Status[0].updated_at
      #term = tm.timestamp() - p1tm.timestamp()
#      Index.objects.create(lossap=clossap, dmg=cdmg, usemp=cusemp, behavior=cbehavior)
      return redirect('polls:index')
      
  d = {
      'rStatus': rStatus,
      'p1ap': p1ap,
      'p1hp': p1hp,
      'p1mp': p1mp,
      'p1ev': p1ev,
      'p1tm': p1tm,
  }
  return render(request, 'polls/apc.html', d)

import numpy as np
import matplotlib.pyplot as plt
import io

def graph_ap(request):
    #apv = Status[:10].ap
    rStatus = Status.objects.all()
    y=[]#ap
    x=[]#id
    for i in range(len(rStatus)):#スマートなやり方じゃないかも
        ap=rStatus[i].ap
        y.append(ap)
        n=rStatus[i].id
        x.append(n)
        
    ap = np.array(y)
    num = np.array(x)
    plt.plot(num, ap)
    
    return render(request, 'polls/graph_ap.html')
    
def graph_hp(request):
    rStatus = Status.objects.all()
    y=[]#hp
    x=[]#id
    for i in range(len(rStatus)):#スマートなやり方じゃないかも
        hp=rStatus[i].hp
        y.append(hp)
        n=rStatus[i].id
        x.append(n)
        
    hp = np.array(y)
    num = np.array(x)
    plt.plot(num, hp)
    
    return render(request, 'polls/graph_hp.html')

def graph_mp(request):
    rStatus = Status.objects.all()
    y=[]#hp
    x=[]#id
    for i in range(len(rStatus)):#スマートなやり方じゃないかも
        mp=rStatus[i].mp
        y.append(mp)
        n=rStatus[i].id
        x.append(n)
        
    mp = np.array(y)
    num = np.array(x)
    plt.plot(num, mp)
    
    return render(request, 'polls/graph_mp.html')

def graph_all(request):
    graph_ap(request)
    graph_hp(request)
    graph_mp(request)

    return render(request, 'polls/graph_all.html')

#png画像形式に変換数関数
def plt2png():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    s = buf.getvalue()
    buf.close()
    return s

#画像埋め込み用view
def img_plot(request):
    # matplotを使って作図する

    ax = plt.subplot()
    png = plt2png()
    plt.cla()
    response = HttpResponse(png, content_type='image/png')
    return response