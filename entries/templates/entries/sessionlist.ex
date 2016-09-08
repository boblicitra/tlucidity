{% extends 'layout.html' %}

{% block content %}
	{% for session in object_list %}
	<div class="col-sm-8">
		<a href="{% url 'sessions_detail' session.pk %}">
			{{ session.title }}
		</a>
	</div>
	<div class="col-sm-2">
		<a href="{% url 'sessions_update' session.pk %}">
			Update
		</a>
	</div>
	<div class="col-sm-2">
		<a href="{% url 'sessions_delete' session.pk %}">
			Delete
		</a>
	</div>
	{% endfor %}
	<div class="col-md-12">
		<a href="{% url 'sessions_create' %}">
			Submit session
		</a>
	</div>
{% endblock %}
