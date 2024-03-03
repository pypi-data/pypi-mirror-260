from django.shortcuts import render
from django.http import HttpResponse
from django.core.management import call_command

def djamal_admin(request):
    return render(request, 'templates/admin.html')

def add_alias(request):
    # Execute the add_alias command
    call_command('add_alias')
    return HttpResponse("Alias added successfully.")

def dockerize(request):
    # Execute the dockerize command
    call_command('dockerize')
    return HttpResponse("Dockerize command executed successfully.")

def help_text(request):
    # Execute the help command
    output = call_command('help')
    return HttpResponse(output)

def print_version(request):
    # Execute the version command
    output = call_command('version')
    return HttpResponse(output)

def setup_djamal(request):
    # Execute the setup_djamal command
    call_command('setup_djamal')
    return HttpResponse("Djamal setup command executed successfully.")

def accessory(request, *args):
    # Execute the accessory command
    output = call_command('accessory', *args)
    return HttpResponse(output)

def app(request, *args):
    # Execute the app command
    output = call_command('app', *args)
    return HttpResponse(output)

def audit(request, *args):
    # Execute the audit command
    output = call_command('audit', *args)
    return HttpResponse(output)

def build(request, *args):
    # Execute the build command
    output = call_command('build', *args)
    return HttpResponse(output)

def config(request, *args):
    # Execute the config command
    output = call_command('config', *args)
    return HttpResponse(output)

def deploy(request, *args):
    # Execute the deploy command
    output = call_command('deploy', *args)
    return HttpResponse(output)

def details(request, *args):
    # Execute the details command
    output = call_command('details', *args)
    return HttpResponse(output)

def env(request, *args):
    # Execute the env command
    output = call_command('env', *args)
    return HttpResponse(output)

def envify(request, *args):
    # Execute the envify command
    output = call_command('envify', *args)
    return HttpResponse(output)

def healthcheck(request, *args):
    # Execute the healthcheck command
    output = call_command('healthcheck', *args)
    return HttpResponse(output)

def init(request, *args):
    # Execute the init command
    output = call_command('init', *args)
    return HttpResponse(output)

def lock(request, *args):
    # Execute the lock command
    output = call_command('lock', *args)
    return HttpResponse(output)

def prune(request, *args):
    # Execute the prune command
    output = call_command('prune', *args)
    return HttpResponse(output)

def redeploy(request, *args):
    # Execute the redeploy command
    output = call_command('redeploy', *args)
    return HttpResponse(output)

def registry(request, *args):
    # Execute the registry command
    output = call_command('registry', *args)
    return HttpResponse(output)

def remove(request, *args):
    # Execute the remove command
    output = call_command('remove', *args)
    return HttpResponse(output)

def rollback(request, *args):
    # Execute the rollback command
    output = call_command('rollback', *args)
    return HttpResponse(output)

def server(request, *args):
    # Execute the server command
    output = call_command('server', *args)
    return HttpResponse(output)

def setup(request, *args):
    # Execute the setup command
    output = call_command('setup', *args)
    return HttpResponse(output)

def traefik(request, *args):
    # Execute the traefik command
    output = call_command('traefik', *args)
    return HttpResponse(output)

def create_djamal_extension(request, *args):
    # Execute the create_djamal_extension command
    output = call_command('create_djamal_extension', *args)
    return HttpResponse(output)
