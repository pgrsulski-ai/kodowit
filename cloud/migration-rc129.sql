
-- RC129: zarządzanie wyłącznie własnymi publikacjami.
create or replace function public.kodowit_my_apps() returns table(id uuid,name text,version text,created_at timestamptz) language sql stable security definer set search_path = '' as $$
 select a.id,a.name,a.version,a.created_at from public.kodowit_apps a where a.owner=auth.uid() order by a.created_at desc;
$$;
create or replace function public.kodowit_remove_app(app_id uuid) returns boolean language plpgsql security definer set search_path = '' as $$
begin
 delete from public.kodowit_apps where id=app_id and owner=auth.uid(); return found;
end; $$;
create or replace function public.kodowit_update_app(app_id uuid,app_name text,app_version text,app_html text) returns boolean language plpgsql security definer set search_path = '' as $$
begin
 update public.kodowit_apps set name=app_name,version=app_version,html=app_html where id=app_id and owner=auth.uid(); return found;
end; $$;
revoke all on function public.kodowit_my_apps(), public.kodowit_remove_app(uuid), public.kodowit_update_app(uuid,text,text,text) from public, anon;
grant execute on function public.kodowit_my_apps(), public.kodowit_remove_app(uuid), public.kodowit_update_app(uuid,text,text,text) to authenticated;
