from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from ideas.models import Idea  

from .ai import model # Gemini model
import google.generativeai as genai



@login_required
def caption_page(request):
    return render(request,'caption_page.html' )

@login_required
def ideas_list_partial(request):
    ideas = Idea.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "ideas/partials/clickable_idea_list.html", {"ideas": ideas})


@login_required
def use_idea(request, idea_id):
    if request.method != "POST":
        raise Http404()

    try:
        idea = Idea.objects.get(id=idea_id, user=request.user)
        return render(request, "ideas/partials/idea_textarea.html", {"idea": idea})
    except Idea.DoesNotExist:
        raise Http404()

    # Return only the idea text that will be inserted into the caption input
    


@login_required
@require_POST
def generate_caption(request):
    idea_text = request.POST.get("idea_text", "").strip()
    style = request.POST.get("caption_style", "short_hook")

    if not idea_text:
        return render(request, "partials/caption_error.html", {
            "message": "No idea text was provided."
        })
    
    
    style_prompts = {
        "short_hook": """
        Write ONE scroll-stopping short hook.
        Rules:
        - Max 10–12 words
        - Punchy and disruptive
        - No hashtags
        - No emojis
        """,

        "engaging_story": """
        Write ONE storytelling caption.
        Rules:
        - 1–2 short sentences
        - Emotional or relatable
        - No hashtags
        """,

        "promotional": """
        Write ONE promotional caption.
        Rules:
        - Persuasive tone
        - Clear CTA
        - No more than 2 short sentences
        """,

        "question": """
        Write ONE question caption.
        Rules:
        - Must trigger comments
        - Simple and bold
        - No hashtags
        """,
    }

    prompt = f"""
You are an expert social media caption writer.

Write 5 high-converting social media captions based on this idea:
\"\"\"{idea_text}\"\"\"

   STYLE SELECTED: {style}

    {style_prompts[style]}

### FORMAT RULES (follow strictly)
- Output in clean Markdown.
- Use numbered items.
- Each caption must be separated by a blank line.
- Each item should look exactly like this:

1. **Hook Title**
   Your caption goes here in one short line.

### DO NOT:
- Add long intros
- Add explanations
- Add hashtags
- Add emojis unless relevant
- Break the format
"""


    try:
        response = model.generate_content(prompt)
        caption = response.text
   
     
      

    except Exception as e:
        print("Gemini Error:", e)
        return render(request, "partials/caption_error.html", {
            "message": "AI generation failed.",
            "error": str(e)
        })

    return render(request, "partials/caption_result.html", {
        "caption": caption,
    })


def set_caption_style(request):
    style = request.POST.get("style", "short_hook")
    return HttpResponse(
        f"<input type='hidden' name='caption_style' value='{style}'>"
    )